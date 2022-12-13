import pandas
import os
import matplotlib.pyplot as plt
from datetime import datetime
import numpy

if __name__ == '__main__':
    # load data
    if not os.path.exists('merged_data.csv'):
        exit(0)
    master_dataframe = pandas.pandas.read_csv('merged_data.csv')

    count_dataframe = pandas.DataFrame()                                                            # new, empty dataframe
    count_dataframe['start_date'] = master_dataframe['start_date']                                  # copy start_date column
    count_dataframe['start_date'] = [datetime.strptime(dt, '%Y-%m-%d %H:%M:%S') for dt in count_dataframe['start_date']]     # convert dates to datetime objects
    count_dataframe['start_date'] = [dt.strftime('%Y-%m') for dt in count_dataframe['start_date']]  # strip the day and time (leave year and month)
    count_dataframe['start_date'] = pandas.to_datetime(count_dataframe['start_date'])               # convert column to datetime
    count_dataframe['file_name'] = master_dataframe['file_name']                                    # copy file_name column (repo name)
    count_series = count_dataframe.value_counts()                                                   # count the number of date occurances within repo names
    count_dataframe = pandas.DataFrame()                                                            # clear dataframe
    count_dataframe['start_date'] = [tuple[0] for tuple in count_series.index]                      # copy start dates to new dataframe (repeats removed essentially)
    count_dataframe['file_name'] = [tuple[1] for tuple in count_series.index]                       # copy the repo name to the new dataframe
    count_dataframe['count'] = count_series.values                                                  # copy the counts of each date occurance within repo names
    count_dataframe.sort_values(by='start_date', ascending=True, inplace=True, ignore_index=True)   # sort by date in ascending order (older to newer)
    count_dataframe.to_csv('counted_data.csv')                                                      # save to csv
    count_dataframe = count_dataframe.pivot(index='start_date', columns='file_name')                # reformat dataframe to have repo names as columns, date occurances as the indices, and counts as the data
    count_dataframe.fillna(value=0, inplace=True)

    count_dataframe = count_dataframe['count'].drop(columns='hugging_face', axis=1)

    count_dataframe.to_csv('counted_data_formatted.csv')                                            # save to csv

    # count_dataframe.plot.area(stacked=True)                                                         # plot data
    # plt.show()

    # count_dataframe['count'].plot.box()                                                             # plot box plots
    # plt.xticks(rotation=45)
    # plt.show()

    mean_datetime_dataframe = pandas.DataFrame()                                             # new, empty dataframe
    mean_series = count_dataframe.mean(axis=1)                           # calculate mean of all repos for each date occurance
    mean_datetime_dataframe['start_date'] = [value for value in mean_series.index]
    mean_datetime_dataframe['start_date'] = pandas.to_datetime(mean_datetime_dataframe['start_date'])
    mean_datetime_dataframe['mean'] = [value for value in mean_series.values]

    # plt.plot(mean_datetime_dataframe['start_date'], mean_datetime_dataframe['mean'])
    # plt.axvline(x=datetime(2020, 4, 1), color='red', linestyle='--')
    # plt.axvline(x=datetime(2021, 5, 1), color='red', linestyle='--')
    # plt.ylim([0,4])
    # plt.title('Mean Count of New Contributors by Start Month')
    # plt.xlabel('Date (Month)')
    # plt.ylabel('Mean Count')
    # plt.show()

    norm_avg_dataframe = pandas.DataFrame()
    norm_avg_dataframe['Pre-COVID'] = mean_datetime_dataframe[mean_datetime_dataframe['start_date'] < datetime(2020, 4, 1)].mean() / len(mean_datetime_dataframe[mean_datetime_dataframe['start_date'] < datetime(2020, 4, 1)])
    norm_avg_dataframe['During-COVID'] = mean_datetime_dataframe[(mean_datetime_dataframe['start_date'] >= datetime(2020, 4, 1)) & (mean_datetime_dataframe['start_date'] < datetime(2021, 5, 1))].mean() / len(mean_datetime_dataframe[(mean_datetime_dataframe['start_date'] >= datetime(2020, 4, 1)) & (mean_datetime_dataframe['start_date'] < datetime(2021, 5, 1))])
    norm_avg_dataframe['Post-COVID'] = mean_datetime_dataframe[mean_datetime_dataframe['start_date'] >= datetime(2021, 5, 1)].mean() / len(mean_datetime_dataframe[mean_datetime_dataframe['start_date'] >= datetime(2021, 5, 1)])
    norm_avg_dataframe = norm_avg_dataframe.transpose()
    print(norm_avg_dataframe)
    norm_avg_dataframe.plot.bar()
    plt.title('Mean Count of New Contributors by Era')
    plt.xlabel('')
    plt.ylabel('Mean Count (Normalized)')
    plt.xticks(rotation=0)
    plt.show()

    # fig, ax = plt.subplots(nrows=len(count_dataframe.columns), ncols=1)
    # for idx in range(len(count_dataframe.columns)):
    #     ax[idx].plot(count_dataframe.iloc[:,idx])
    #     plt.ylim([0,20])
    # plt.show()
