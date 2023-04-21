### Code
GitHub Link: https://github.com/dso-noroff/bach_project

### Required Python packages

| Package   |      Install      |
|----------|:-------------:|
| Codecs |  |
| Faker |  pip install Faker |
| Folium |    pip install folium   |
| Itertools |  |
| Jupyter Notebook | pip install jupyter |
| Matplotlib | pip install matplotlib |
| Numpy | pip install numpy |
| Openrouteservice | pip install openrouteservice |
| Pandas | pip install pandas |
| Plotly | pip install plotly |
| Random |  |
| Tensorflow | pip install tensorflow |
| Tensorflow-Recommenders | pip install tensorflow-recommenders |
| Ydata-profiling | pip install ydata-profiling |


### Files and folders
***01_exploration.ipynb:***
The Jupyter Notebook contains the data exploration and analysis and the logic to set up and test the code for calculating the driving distance, plotting the travel route on the map, and computing the categorical environmental friendliness.


***02_recommender.ipynb:***
This Jupyter Notebook, used for the Machine Learning part, is responsible for loading the orders and creating the data frames, which are further converted into MaptDataset to train the model. Then it sets up all the training settings, divides the dataset into training and testing sets, and compiling and fits the model. Then the evaluation and results phase, before everything is put together, to make recommendations, compute the environmental costs, and display the travel route on the map for three examples.


***Generator Files:***
The generator files are used to generate and enrich the dataset. It enriches the Products with random colors and prices based on the data from the Electronic Product Declarations gathered from our employer. They further generate the warehouse product availability, users with their location within a specific range of a warehouse. And the final one generates the orders based on the other datasets and can create any required orders.


***Helper Files:***
These files interact with the datasets more easily, sharing one file between the Jupyter Notebooks to get and write to the files.They also assist in calculating the driving distance between two locations and create different graphs using either folium, plotly, or pyplot. Furthermore, helper functions help with categorizing the transportation costs, calculating which transportation method is available for the closest warehouse, getting warehouses with a particular product in stock, getting the closest warehouses to a user, and calculating the emissions.


***Recommender Model Files:***
They hold the inner structure of the recommender model. The main starting point is the recommender_recommender_model.py which holds the core logic of the recommendation model and instantiates the query and candidate model. The query model then instantiates the user model and the candidate the product model.


***Data Folder:***
The folder contains all the .csv used in the project. It also has some additional files that were not used, like the orders containing one million and hundred thousand together with ten thousand and hundred thousand users, which were created to be the final dataset to train a more extensive model.


***Models Folder:***
Contain two model classes used in the project for order and product. Initially, they were inside the generators, but they were extracted for better separation of concern.


***Map.html***
It is the maps created in both Jupyter Notebooks.


***Warehouses.html***
It contains the map of warehouses created in the exploration notebook.


***Order_Profile.html:***
It contains the YData profiling to see more information about the dataset in the exploration notebook.


***API KEYS:***
The following files need API-keys to be able to run the code.

- helper_distance.py - Google Maps API key
- helper_graphs.py - Openrouteservice API key
