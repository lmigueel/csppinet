import pandas as pd
import networkx as nx
import os


folder_path = os.getcwd()

def network_metrics(expression_data):
    """
    Calculates the metrics for all csppinet generated in current working folder directory

    Parameters
    ----------
    expression_data: CSV expression file 

    Returns
    ---------
    Several metrics reports, such as BC, CC and Degree.

    """

    print("Step 4: Network analysis step ...")
    exp_data = pd.read_csv(expression_data,index_col=0)
    cols = exp_data.columns

    all_metrics = []

    for filename in os.listdir(folder_path):
        
        if filename.startswith('csppinet_csnetwork_') and filename.endswith('.csv'):
            variety_name = filename.split('csnetwork_')[1].split('.')[0]
            file_path = os.path.join(folder_path, filename)

            # Load the CSV file as a network
            ppi_data = pd.read_csv(file_path)
            g = nx.from_pandas_edgelist(ppi_data,'p1','p2',edge_attr=True)

            output = folder_path + "/csppinet_Reports_"+variety_name+".tsv"
            report_file = open(output, "w")

            print("File:", filename,file=report_file)
            print("Number of vertices:", g.number_of_nodes(),file=report_file)
            print("Number of edges:", g.number_of_edges(),file=report_file)
            print("Network is connected?",nx.is_connected(g),file=report_file)
            print("Network density:",nx.density(g),file=report_file)
            print("Total of components:", nx.number_connected_components(g),file=report_file)

        
            metrics_genes = pd.DataFrame(columns=['Genes', 'CC', 'BC', 'Degree'])
            genes_list = g.nodes
            cc = nx.closeness_centrality(g)
            bc = nx.betweenness_centrality(g)
            degree = g.degree()

            metrics_genes['Genes'] = list(genes_list)
            metrics_genes['CC'] = list(cc.values())
            metrics_genes['BC'] = list(bc.values())
            metrics_genes['Degree'] = [d for n, d in degree]

            name = "csppinet_GenesMetrics_"+variety_name+".csv"
            metrics_genes.to_csv(name,index=False)

            all_metrics.append(metrics_genes)

    # Create an empty dictionary to store the individual DataFrames
    dfs = {}

    # Iterate over the columns (BC, CC, and Degree)
    for column in ['BC', 'CC', 'Degree']:
        # Create a list to store the DataFrames for the current column
        column_dfs = []

        # Merge the DataFrames from the list based on the index column (Genes)

        for df in all_metrics:
            df[column] = df[column].astype(str)
            merged_df = pd.merge(df[['Genes', column]], df[['Genes', column]], on='Genes', how='outer')
            merged_df.set_index('Genes', inplace=True)
            merged_df = merged_df.drop(merged_df.columns[1], axis=1)
            column_dfs.append(merged_df)

        # Concatenate the DataFrames from the current column into a single DataFrame
        merged_column_df = pd.concat(column_dfs, axis=1, keys=range(1, len(all_metrics) + 1))

        # Fill missing values with NA
        merged_column_df.fillna('NA', inplace=True)

        # Store the merged DataFrame for the current column in the dictionary
        dfs[column] = merged_column_df


    # Iterate over the dictionary
    for column, df in dfs.items():

        # Change the column name
        df.columns = cols

        # Save the DataFrame as a CSV file
        file_name = f'{column}_metrics_merged.csv'
        df.to_csv(file_name, index=True)
