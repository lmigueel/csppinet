
import numpy as np

def calculate_F(p, expression_values):
    """
    Calculate the fluctuation of the expression curve of gene p (F_p)

    Parameters
    ----------
    p: gene index
    expression_values: list of expression values 

    Returns
    ---------
    F_p: fluctuation of the expression curve of gene p

    References
    ---------
       [1] Wang, J., Peng, X., Li, M., & Pan, Y. (2013). Construction and application of dynamic protein interaction network based on time course gene expression data. PROTEOMICS, 13(2), 301–312. doi:10.1002/pmic.201200277 
    """

    u_p = np.mean(expression_values.loc[p])
    a_p = np.std(expression_values.loc[p])

    # Calculate the value of F(p)
    F_p = 1 / (1 + a_p ** 2)
    
    return F_p

def calculate_active_threshold(p, expression_values):
    """
    Calculate the algorithmic mean and standard deviation of the expression values of gene p and
    determine the activation threshold

    Parameters
    ----------
    p: gene index
    expression_values: list of expression values 

    Returns
    ----------
    activate_th: the active threshold of gene p which is determined by the values of its algorithmic mean, three-sigma,
    and F. 
    """

    u_p = np.mean(expression_values.loc[p])
    a_p = np.std(expression_values.loc[p])

    # Calculate the value of F(p)
    F_p = calculate_F(p, expression_values)

    # Calculate the active threshold for gene p
    active_th = u_p + 3 * a_p * (1 - F_p)

    return active_th

def determine_gene_activity(p, expression_values, method, active_threshold):
    """
    Determine the activity of gene p at each sample i

    Parameters
    ----------
    p: gene index
    expression_values: list of expression values
    active_threshold: threshold to determine if a gene p is activated or not

    Returns
    ----------
    gene_activity: an array containing the activity of a gene p
    """

    if method == "3-sigma" or method=="pre-threshold":
        num_conditions = expression_values.shape[1]
        gene_activity = np.zeros(num_conditions)

        for i in range(num_conditions):
            if expression_values.loc[p][i] > active_threshold:
                gene_activity[i] = 1

        return gene_activity

    else:
        num_conditions = expression_values.shape[1]
        gene_activity = np.zeros(num_conditions)

        for i in range(num_conditions):
            column_data = expression_values.iloc[:,i]
            quantile = active_threshold/100
            threshold = column_data.quantile(quantile)
            if expression_values.loc[p][i] > threshold:
                gene_activity[i] = 1
        
        return gene_activity
