from setuptools import setup, find_packages

setup(
    name='iSport',  # Nom du projet
    version='1.0.0',  # Version du projet, suivez le format SEMVER 
    description='Application Kivy pour le sport',  # Brève description
    author='Wassim BAHMANI',  # Nom de l'auteur
    author_email='eps.innov@gmail.com',  # Email de l'auteur (optionnel mais recommandé)
    url="https://github.com/MissawB/EPS'Innov",  # URL du dépôt ou de la page du projet
    packages=find_packages(),  # Recherche automatiquement les sous-packages
    include_package_data=True,  # Inclut les fichiers de données spécifiés dans MANIFEST.in
    python_requires='>=3.7',  # Version minimale de Python requise
    install_requires=[
        'kivy>=2.1.0',  # Spécifie la version minimale de Kivy requise
    ],
    entry_points={
        'console_scripts': [
            'isport=isport.main:main',  # Point d'entrée CLI
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords='kivy application sport' # Mots-clés pour la recherche de packages
)