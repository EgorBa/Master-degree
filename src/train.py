import configparser
import os
import pandas as pd
import pickle
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import sys
import traceback

from logger import Logger

SHOW_LOG = True


class KNNModel():

    def __init__(self) -> None:
        logger = Logger(SHOW_LOG)
        self.config = configparser.ConfigParser()
        self.log = logger.get_logger(__name__)
        self.config.read("config.ini")
        self.X_train = pd.read_csv(
            self.config["SPLIT_DATA"]["X_train"], index_col=0)
        self.y_train = pd.read_csv(
            self.config["SPLIT_DATA"]["y_train"], index_col=0)
        self.X_test = pd.read_csv(
            self.config["SPLIT_DATA"]["X_test"], index_col=0)
        self.y_test = pd.read_csv(
            self.config["SPLIT_DATA"]["y_test"], index_col=0)
        sc = StandardScaler()
        self.X_train = sc.fit_transform(self.X_train)
        self.X_test = sc.transform(self.X_test)
        self.project_path = os.path.join(os.getcwd(), "experiments")
        self.knn_path = os.path.join(self.project_path, "knn.sav")
        self.log.info("KNNModel is ready")

    def knn(self, use_config: bool, n_neighbors=3, metric="minkowski", p=2, predict=False) -> bool:
        if use_config:
            try:
                classifier = KNeighborsClassifier(n_neighbors=self.config.getint(
                    "KNN", "n_neighbors"), metric=self.config["KNN"]["metric"], p=self.config.getint("KNN", "p"))
            except KeyError:
                self.log.error(traceback.format_exc())
                self.log.warning(f'Using config:{use_config}, no params')
                sys.exit(1)
        else:
            classifier = KNeighborsClassifier(
                n_neighbors=n_neighbors, metric=metric, p=p)
        try:
            classifier.fit(self.X_train, self.y_train.values.ravel())
        except Exception:
            self.log.error(traceback.format_exc())
            sys.exit(1)
        if predict:
            y_pred = classifier.predict(self.X_test)
            self.log.info(f'Accuracy = {accuracy_score(self.y_test, y_pred)}')
        params = {'n_neighbors': n_neighbors,
                  'metric': metric,
                  'p': p,
                  'path': self.knn_path}
        return self.save_model(classifier, self.knn_path, "KNN", params)

    def save_model(self, classifier, path: str, name: str, params: dict) -> bool:
        self.config[name] = params
        os.remove('config.ini')
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        with open(path, 'wb') as f:
            pickle.dump(classifier, f)

        self.log.info(f'{path} is saved')
        return os.path.isfile(path)


if __name__ == "__main__":
    knn_model = KNNModel()
    knn_model.knn(use_config=False, predict=True)
