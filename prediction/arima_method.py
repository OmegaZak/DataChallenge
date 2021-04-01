import itertools
import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm


class arima_model:

    def __init__(self, arima_param, seasonal_param):
        
        # Define the p, d and q parameters in Arima(p,d,q)(P,D,Q) models
        
        p = arima_param['p']
        d = arima_param['d']
        q = arima_param['q']
        
        # Generate all different combinations of p, q and q triplets
        
        self.pdq = list(itertools.product(p, d, q))
        # Generate all different combinations of seasonal p, q and q triplets
        
        self.seasonal_pdq = [(x[0], x[1], x[2], seasonal_param)
                             for x in list(itertools.product(p, d, q))]

    
    # Fit model
    
    def fit(self, ts): 
        warnings.filterwarnings("ignore") # specify to ignore warning messages
        results_list = []
        for param in self.pdq:
            for param_seasonal in self.seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(ts,
                                                    order=param,
                                                    seasonal_order=param_seasonal,
                                                    enforce_stationarity=False,
                                                    enforce_invertibility=False)
                    results = mod.fit()

                    print('ARIMA{}x{}seasonal - AIC:{}'.format(param,
                                                               param_seasonal, results.aic))
                    results_list.append([param, param_seasonal, results.aic])
                except:
                    continue
        results_list = np.array(results_list)
        lowest_AIC = np.argmin(results_list[:, 2])

        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('SARIMAX{}x{}seasonal with lowest_AIC:{}'.format(
            results_list[lowest_AIC, 0], results_list[lowest_AIC, 1], results_list[lowest_AIC, 2]))
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')


 #Fitting the SARIMAX model

        mod = sm.tsa.statespace.SARIMAX(ts,
                                        order=results_list[lowest_AIC, 0],
                                        seasonal_order=results_list[lowest_AIC, 1],
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
        self.final_result = mod.fit()

        print('Final model summary:')
        print(self.final_result.summary().tables[1])
        print('Final model diagnostics:')
        
        self.final_result.plot_diagnostics(figsize=(15, 12))
        
        plt.tight_layout()
        plt.savefig('model_diagnostics.svg', dpi=300)
        plt.show()


#Validating forecasts

    def pred(self, ts, plot_start, pred_start, dynamic, ts_label):

        pred_dynamic = self.final_result.get_prediction(
            start=pd.to_datetime(pred_start), dynamic=dynamic, full_results=True)
        pred_dynamic_ci = pred_dynamic.conf_int()
        ax = ts[plot_start:].plot(label='observed', figsize=(15, 10))

        if dynamic == False:
            pred_dynamic.predicted_mean.plot(
                label='One-step ahead Forecast', ax=ax)
        else:
            pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)

        ax.fill_between(pred_dynamic_ci.index,
                        pred_dynamic_ci.iloc[:, 0],
                        pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)
        ax.fill_betweenx(ax.get_ylim(), pd.to_datetime(plot_start), ts.index[-1],
                         alpha=.1, zorder=-1)
        ax.set_xlabel('Time')
        ax.set_ylabel(ts_label)
        
        plt.legend()
        plt.tight_layout()
        
        if dynamic == False:
            plt.savefig(ts_label + '_one_step_pred.svg', dpi=300)
        else:
            plt.savefig(ts_label + '_dynamic_pred.svg', dpi=300)
        
        plt.show()



# Producing and visualizing forecasts


    def forcast(self, ts, n_steps, ts_label):

        # Get forecast n_steps ahead in future

        pred_fc = self.final_result.get_forecast(steps=n_steps)

        # Get confidence intervals of forecasts

        pred_ci = pred_fc.conf_int() #conf_int() CI function
        ax = ts.plot(label='observed', figsize=(15, 10))
        pred_fc.predicted_mean.plot(ax=ax, label='Forecast in Future')
        ax.fill_between(pred_ci.index,
                        pred_ci.iloc[:, 0],
                        pred_ci.iloc[:, 1], color='k', alpha=.25)
        ax.set_xlabel('Time')
        ax.set_ylabel(ts_label)
        
        plt.tight_layout()
        plt.savefig(ts_label + '_forcast.svg', dpi=300)
        
        plt.legend()
        plt.show()


    def plot_forecast(self, n_steps):

        pred_fc = self.final_result.get_forecast(steps=n_steps)

        plt.figure(figsize=(20,5))
        plt.plot(pred_fc.predicted_mean)
        plt.scatter(pred_fc.predicted_mean.index, pred_fc.predicted_mean.values, color="blue", s=150)
        plt.xlabel("Dates", size=20)
        plt.ylabel("Total today's bikes", size=20)
        
    
    def d_forecast(self, n_steps, n):
        
        pred_fc = self.final_result.get_forecast(steps=n_steps)
        data_forecast = pred_fc.predicted_mean
        return data_forecast.head(n)
        

    def print_pred_dday(self, n_steps):

        pred_fc = self.final_result.get_forecast(steps=n_steps)

        pred_fc.predicted_mean = pred_fc.predicted_mean[(pred_fc.predicted_mean.index.time >= pd.to_datetime("00:01:00").time()) 
        & (pred_fc.predicted_mean.index.time <= pd.to_datetime("12:01:00").time())]

        dday = pred_fc.predicted_mean #DDAY 2 April 9 a.m
        
        print(dday)
