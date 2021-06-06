## **Prediction and visualization of bicycle traffic**

### Prediction part


In this section, we used the SARIMA (*Seasonnal AutoRegressive Integrated Moving Average*) method to train our database (database trained at the end of 2020) and to make a forecast for April 2, 2021 at 9:00 AM. The prediction could have been improved by adding exogenous parameters like **weather**, **temperature**...



+ **`preprocess.py`** preprocessing file
 + **`arima_method.py`**  python class containing the method 
 + **`arima_script_1.ipynb`** execution script
+  **`arima_script_2.ipynb`** execution script


<img src="prediction/images/onestepforc.png?raw=true"/>
 
<img src="prediction/images/dynamforc.png?raw=true"/>

<img src="prediction/images/futurforc.png?raw=true"/>

<img src="prediction/images/predc.png?raw=true"/>


### Visualisation part

In the visualization part, we imported JSON files of each bike counter of Montpellier to make an animation via circles whose diameter changes according to the intensity of the bike traffic in each zone where a bike counter is located, via the **folium** package.

The animation is in .mp4 format (**`Animation.mp4`**) in the **visualisation** folder to download (the animation is not optimal due to many problems encountered)


<img src="visualisation/images/visualbike.png?raw=true"/>

