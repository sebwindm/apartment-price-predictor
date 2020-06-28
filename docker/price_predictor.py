
# from sklearn.ensemble import RandomForestRegressor
# model = RandomForestRegressor()
# model.fit(X_train, Y_train)
# print("Training test score: ", str(model.score(X_train, Y_train)))
# print("Test set score: ", str(model.score(X_test, Y_test)))

# from sklearn.ensemble import GradientBoostingRegressor
# model = GradientBoostingRegressor()
# model.fit(X_train, Y_train)
# print("Training test score: ", str(model.score(X_train, Y_train)))
# print("Test set score: ", str(model.score(X_test, Y_test)))
# from sklearn.neural_network import MLPRegressor
# model = MLPRegressor(max_iter=1000, random_state=0)

# Rescale data so that mean of X = 0 and standard deviation = 1
# (makes it easier for neural network)
# mean_on_train = X_train.mean(axis=0)
# std_on_train = X_train.std(axis=0)
# X_train_scaled = (X_train - mean_on_train) / std_on_train
# X_test_scaled = (X_test - mean_on_train) / std_on_train
# model.fit(X_train_scaled, Y_train)
# print("Training test score: ",str(model.score(X_train_scaled, Y_train)))
# print("Test set score: ", str(model.score(X_test_scaled, Y_test)))

