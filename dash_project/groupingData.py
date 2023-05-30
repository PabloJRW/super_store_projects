# GROUP DATA BY VARIABLE
# =======================================================================

def groupingData(data, features, group_by, method=sum):
    """Function that group data by 'group_by' and return percentage variables"""
    
    # Grouping data by feat
    grouping = data.groupby(group_by).sum().drop('Postal Code', axis=1)

    # Calculate the percentage by variable
    for feat in features:
        grouping['{0}Percent'.format(feat)] = round(grouping[feat] / sum(grouping[feat]) * 100, 2)
    
    return grouping