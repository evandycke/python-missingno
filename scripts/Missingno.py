# coding: utf-8

"""
	Ce script a pour objectif de détecter des valeurs nulles dans un dataframe en utilisant Missingno.
"""

from __future__ import annotations
from threading import Lock, Thread
from typing import Optional

import os, logging
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import missingno as msno

class MissingnoMeta(type): # Définition de la classe Missingno
    """Classe permettant d'implémenter un Singleton thread-safe"""

    _instance: Optional[Missingno] = None

    _lock: Lock = Lock()
    """On a posé un verrou sur cet objet. Il sera utilisé pour la synchronisation des threads lors du premier accès au Singleton."""

    def __call__(cls, *args, **kwargs):
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if not cls._instance:
                cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class Missingno(metaclass=MissingnoMeta): # Définition de la classe Missingno
	"""Classe définissant Missingno, qui permettra d'inspecter un dataframe et identifier les valeurs nulles"""

	def __init__(self): # Constructeur
		# On configure le logger
		LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
		logging.basicConfig(level=logging.DEBUG, filemode='w', format=LOG_FORMAT)
		formatter = logging.Formatter(LOG_FORMAT)
		self.logger = logging.getLogger('missingno')

		# Les logs seront inscrits dans un fichier
		fileHandler = logging.FileHandler("../log/missingno.log", mode='w')
		fileHandler.setFormatter(formatter)
		self.logger.addHandler(fileHandler)
		self.logger.info("Logger initialization complete ...")

	def inspect(self):
		"""Lance l'inspection d'un dataframe"""

		df = pd.read_csv("../in/sp-pos-quot-dep-2021-09-19-19h08.csv", error_bad_lines=False)
		self.logger.info("Dataset loaded !")

		pd.set_option('display.expand_frame_repr', False)

		msno.matrix(df)
		plt.show()

if __name__ == "__main__":
	v = Missingno()
	v.inspect()