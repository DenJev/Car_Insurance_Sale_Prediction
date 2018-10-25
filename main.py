import pandas as pd
from scipy.special import boxcox

from Class_Data_Modeler import DataModeler


def main():
    ####################################################################################################################
    # Main used for house price data set

    #  at this point once the data has been explored, want train_Y to be in its own variable separate from train_X to
    #  pre-process the data train_X and test_X should not be combined at any point as the data should be preprocessed in
    #  one go for train_X but in a real world scenario, test_X may not come in as a large dataset
    model_house = DataModeler(pd.read_csv("Data_In/House_Prices/train.csv"), pd.read_csv("Data_In/House_Prices/test.csv"))

    # model_house.box_plot('SalePrice', 'YearBuilt')
    # model_house.bar_graph_attribute('YrSold')
    # model_house.line_graph_percentage_difference('YrSold')

    # dropped after looking at a scatter plot of the two attributes
    # model_house.scatter_plot('SalePrice', 'GrLivArea')
    model_house.drop_outliers_target_less_y_attribute_greater_x('SalePrice', 300000, 'GrLivArea', 4000)
    model_house.drop_outliers_target_greater_y_attribute_greater_x('SalePrice', 200000, 'LotFrontage', 300)
    # model_house.scatter_plot('SalePrice', 'GrLivArea')

    print(model_house._train_data_set.shape)

    model_house.switch_na_to_median_other_attribute('LotFrontage', 'Neighborhood')
    # all features in train are all pub and 2 na, 'NoSewa' is in test set hence the attribute doesnt help in any way
    # with the model so it is dropped
    attributes_to_none = ["PoolQC", "MiscFeature", "Alley", "Fence", "FireplaceQu", "GarageCond", "GarageQual",
                          "GarageFinish", "GarageYrBlt", "GarageType", "BsmtFinType2", "BsmtExposure", "BsmtFinType1",
                          "BsmtCond", "BsmtQual", "MasVnrType"]

    attributes_to_zero = ['MasVnrArea', 'BsmtHalfBath', 'BsmtFullBath', 'GarageArea', 'GarageCars', 'TotalBsmtSF',
                          'BsmtUnfSF', 'BsmtFinSF2', 'BsmtFinSF1']

    attributes_to_mode = ['Electrical', 'MSZoning', 'Functional', 'SaleType', 'KitchenQual', 'Exterior2nd',
                          'Exterior1st']

    attributes_to_categorical = ['MSSubClass', 'OverallCond', 'YrSold', 'MoSold']

    for x in attributes_to_none:
        model_house.impute_none(x)
    for x in attributes_to_zero:
        model_house.impute_zero(x)
    for x in attributes_to_mode:
        model_house.impute_mode(x)
    for x in attributes_to_categorical:
        model_house.convert_attribute_to_categorical(x)

    # drops id column from train_X and test_X to move it to _test_y_id
    model_house.index_column_drop_and_move_to_pred_y('Id')
    model_house.move_target_to_train_y('SalePrice')  # moves saleprice to train_Y
    model_house.missing_data_ratio_print()
    ####################################################################################################################
    # all the missing values are inputted!!!!
    ####################################################################################################################

    print('The dimension of the train is', model_house._train_data_set.shape)
    print('The dimension of the test is', model_house._test_data_set.shape)

    ####################################################################################################################
    #  need to add these in later
    attributes_to_drop = ['Utilities', 'YearBuilt', 'MoSold', 'YrSold', 'GarageYrBlt', 'YearRemodAdd']
    for x in attributes_to_drop:
        model_house.drop_attribute(x)
    ####################################################################################################################

    attributes_to_normalise = ['LotFrontage', 'LotArea', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF',
                               'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'GarageArea',
                               'WoodDeckSF', 'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea',
                               'MiscVal']

    for x in attributes_to_normalise:
        model_house.normalise_attribute(x)

    attributes_to_one_hot_encode = ['MSSubClass', 'MSZoning', 'Street', 'Alley', 'LotShape', 'LandContour',
                                    'LotConfig', 'LandSlope', 'Neighborhood', 'Condition1', 'Condition2', 'BldgType',
                                    'HouseStyle', 'RoofStyle', 'RoofMatl', 'Exterior1st',
                                    'Exterior2nd', 'MasVnrType', 'ExterQual', 'ExterCond', 'Foundation', 'BsmtQual',
                                    'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2', 'Heating', 'HeatingQC',
                                    'CentralAir', 'Electrical', 'KitchenQual', 'Functional', 'GarageType',
                                    'FireplaceQu', 'GarageFinish', 'GarageQual', 'GarageCond',
                                    'PavedDrive', 'PoolQC', 'Fence', 'MiscFeature', 'SaleType', 'OverallCond',
                                    'SaleCondition', 'OverallQual', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd',
                                    'GarageCars', 'BsmtFullBath', 'KitchenAbvGr', 'BsmtHalfBath', 'HalfBath',
                                    'Fireplaces']

    for x in attributes_to_one_hot_encode:
        model_house.one_hot_encode_attribute(x)

    model_house.delete_unnecessary_one_hot_encoded_columns()

    print('The dimension of the train is', model_house._train_data_set.shape)
    print('The dimension of the test is', model_house._test_data_set.shape)

    ####################################################################################################################

    #  Run the function called, Lasso
    model_house.lasso_compare_alpha([1000, 100, 10]).to_csv('Data_Out/Lasso_model_alpha_1_0point1_0point01.csv',
                                                            index=False)

    # model_house.box_cox_target(0.1)
    model_house.lasso_model(100, 'SalePrice')

    model_house.linear_model('SalePrice')
    ####################################################################################################################

    model_house._train_data_set.to_csv('Data_Out/train_dataset.csv', index=False)
    model_house._test_data_set.to_csv('Data_Out/test_dataset.csv', index=False)


if __name__ == "__main__":
    main()
