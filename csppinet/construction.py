import pandas as pd
import sys
import multiprocessing
from csppinet.functions import (calculate_active_threshold,determine_gene_activity)

def ppi_processing(ppi_data, cols, condition_activity):

    interactome_aux = pd.DataFrame(columns = cols)
    k=0

    # Iterate over each protein-protein interaction and add it to the interactome if both proteins are active in the current condition
    for row in ppi_data.itertuples(index=True, name='Pandas'):

        p1 = row.protein1
        p2 = row.protein2
        row_values = row[3:]

        key_prot = p1+"--"+p2

        key_activation = [key_prot]
        [key_activation.append(val) for val in row_values]

        for j in range(condition_activity.shape[1]):

            if ((p1 in condition_activity.index) and (p2 in condition_activity.index)):

                if condition_activity.loc[p1][j] == 1 and condition_activity.loc[p2][j] == 1:

                    key_activation.append(1)
                else:
                    key_activation.append(0)
            else:

                key_activation.append(0)


        # Add the interactome for the current condition to the interactomes dictionary
        interactome_aux.loc[k] = key_activation
        k=k+1

    return interactome_aux

def construction(ppi_network, expression_data, threads, method, value):
    """
    Constructs the context-specific biological networks based on omics data using one protein activation method given as input

    Parameters
    ----------
    ppi_network: CSV file containing the network
    expression_data: CSV expression file 
    threads: number of threads. If it's not given, we gonna use all threads.
    method: protein activation method. Choose between: "3-sigma", "pre-threshold" or "percentile"
    value: activation threshold. Should be given in the "pre-threshold" or "percentile" methods.

    Returns
    ---------
    Context-specific networks based on "expression_data" biological conditions as CSV/TSV files

    """

    ###### 1. Load data ######
    print("Step 1: Loading the datasets ...")
    exp_data = pd.read_csv(expression_data,index_col=0)
    ppi_data = pd.read_csv(ppi_network)
    
    
    ###### 2. Verify activation per gene in each condition and methods ########
    condition_activity = pd.DataFrame(columns = exp_data.columns)
    i = 0

    allowed_values = ["3-sigma", "pre-threshold","percentile"]

    if method in allowed_values:
        # Proceed with the desired functionality
        print("Step 2: Processing with method", method)
    else:
        # Stop and produce an error message
        print("Invalid argument! Please enter either '3-sigma', 'percentile' or 'pre-threshold'.")
        sys.exit(1)


    # Create an empty dictionary to store the interactomes
    interactomes = {}

    # Iterate over each biological condition
    for gene_index, row in exp_data.iterrows():

        if method == "3-sigma":
            active_threshold = calculate_active_threshold(gene_index, exp_data)
            gene_activity = determine_gene_activity(gene_index, exp_data, method, active_threshold)
            condition_activity.loc[i] = gene_activity
            i=i+1
        elif method == "pre-threshold":
            active_threshold = value  #user input
            gene_activity = determine_gene_activity(gene_index, exp_data, method, active_threshold)
            condition_activity.loc[i] = gene_activity
            i=i+1
        else: #percentile
            active_threshold = value  #user input
            gene_activity = determine_gene_activity(gene_index, exp_data, method, active_threshold)
            condition_activity.loc[i] = gene_activity
            i=i+1

    condition_activity = condition_activity.set_index(exp_data.index)

    # Create a new df to store the interactome for the current condition
    cols =["key"]
    [cols.append(val) for val in ppi_data.columns[2:len(ppi_data.columns)]]
    [cols.append(val) for val in exp_data.columns ]


    # Multiprocessing
    if(threads is not None):
        num_processes = threads
    else:
        num_processes = multiprocessing.cpu_count()  # Number of available CPU cores

    pool = multiprocessing.Pool(processes=num_processes)

    # Split the dataframe into chunks to be processed by each process
    chunk_size = len(ppi_data) // num_processes
    chunks = [ppi_data[i:i+chunk_size] for i in range(0, len(ppi_data), chunk_size)]

    # Apply the process_row function to each chunk in parallel
    #results = pool.map(ppi_processing, chunks)
    results = pool.starmap(ppi_processing, [(chunk, cols, condition_activity) for chunk in chunks])

    # Combine the results into a single dataframe
    interactome = pd.concat(results, ignore_index=True)


    #### 3. Bulding context-specific ppi networks ####
    print("Step 3: Bulding context-specific biological networks...")

    # iterate over columns
    for col in interactome.columns[1:interactome.shape[1]]:
    # filter rows that have value 1 in the column
        filtered = interactome[interactome[col] == 1].copy()

    # split the first column by "--" and add two new columns
        if not filtered.empty:
            filtered[['p1', 'p2']] = filtered['key'].str.split('--', expand=True)

    # display the filtered DataFrame
        if not filtered.empty:
            name = "csppinet_csnetwork_"+col+".csv"
            new_filtered = filtered.drop('key', axis=1)

            last_two_columns = new_filtered.columns[-2:]  # Get the names of the last two columns
            other_columns = new_filtered.columns[:-2]  # Get the names of the other columns

            new_order = last_two_columns.tolist() + other_columns.tolist()  # Concatenate the column names in the desired order

            new_filtered = new_filtered[new_order]  # Reorder the columns in the DataFrame

            # Combine the 'Protein1' and 'Protein2' columns into a new column 'Edge'
            new_filtered['Edge'] = new_filtered[['p1', 'p2']].apply(lambda x: tuple(sorted(x)), axis=1)

            # Remove duplicates
            new_filtered = new_filtered.drop_duplicates(subset=['Edge'])

            # Split the 'Edge' column back into 'Protein1' and 'Protein2' columns
            new_filtered[['p1', 'p2']] = pd.DataFrame(new_filtered['Edge'].tolist(), index=new_filtered.index)

            # Drop the 'Edge' column
            new_filtered = new_filtered.drop('Edge', axis=1)

            new_filtered.to_csv(name, index=False)


