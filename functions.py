import pandas as pd
import streamlit as st
import xml.etree.ElementTree as ET
import os


@st.cache()
def Get_Data(path_to_watch_data):
    tree = ET.parse(path_to_watch_data)
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]
    df = pd.DataFrame(record_list)
    return df


def Set_Up():
    if os.path.isdir('./apple_watch_data'):
        selector_index = 1
        st.write('You already have data. What would you like to do?')
    else:
        os.mkdir('./apple_watch_data')
        st.write('I am setting up your data. This will take a few minutes.')
        selector_index = 0
    function = st.sidebar.selectbox(
        'Choose a function', ['reset database', 'examine a subset'], index=selector_index)
    if function == 'reset database':
        Reset_Database()
    elif function == 'examine a subset':
        Show_Files()


def Fix_Flights(df):
    df.creationDate = pd.to_datetime(df.creationDate)
    df.creationDate = df.creationDate.dt.date
    df.value = df.value.astype(int)
    st.write('original', df)
    df.drop(['sourceName', 'unit', 'startDate', 'endDate',
            'sourceVersion', 'device'], axis=1, inplace=True)
    st.write('after drop', df)
    df.reset_index(inplace=True, drop=True)
    st.write(type(df.loc[0, 'creationDate']), type(df.loc[0, 'value']))
    df1 = pd.DataFrame(df.groupby(by="creationDate")['value'].sum())
    df1['type'] = type_stem+'FlightsClimbed'
    df1['unit'] = 'count'
    df1.reset_index(inplace=True, drop=False)
    st.write('after groupby', type(df1), df1)
    return df1


def Fix_Sugar(df):
    df.creationDate = pd.to_datetime(df.creationDate)
    df.creationDate = df.creationDate.dt.date
    df.value = df.value.astype(float)
    st.write('original', df)
    df.drop(['sourceName', 'unit', 'startDate', 'endDate',
            'sourceVersion', 'device'], axis=1, inplace=True)
    st.write('after drop', df)
    df.reset_index(inplace=True, drop=True)
    st.write(type(df.loc[0, 'creationDate']), type(df.loc[0, 'value']))
    df1 = pd.DataFrame(df.groupby(by="creationDate")['value'].sum())
    df1['type'] = type_stem+'DietarySugar'
    df1['unit'] = 'g'
    df1.reset_index(inplace=True, drop=False)
    st.write('after groupby', type(df1), df1)
    return df1


def Reset_Database():
    a = st.empty()
    a.write('Getting initial data...')
    df = Get_Data('apple_health_export/export.xml')
    types = [x[24:] for x in list(set(df.type.tolist()))]
    types = [x if x != 'StepCount' else '_'+x for x in types]
    # st.write(types)
    for var_type in types:
        # st.write(var_type)
        if var_type == '_StepCount':
            filter = type_stem+'StepCount'
        else:
            filter = type_stem+var_type
        df1 = df[df.type == filter]
        a.write(
            f'I am working {var_type} with {df1.shape[0]} rows. This will take about {int(1+(df1.shape[0]/90000))} secs.')
        if df1.shape[0] > 0:
            unit, measure, groupby_method = Read_Replace(var_type)
            # st.write(unit, measure, groupby_method)
            for col in ['creationDate', 'startDate', 'endDate']:
                df1[col] = pd.to_datetime(df1[col])
            df1.reset_index(inplace=True, drop=True)
            df1 = Fix_Show(df1, var_type, unit, measure, groupby_method)
            df1.to_csv(f'{data_path}{var_type}.csv', index=False)
        else:
            pass
    a.empty()
    st.write('Done resetting data.')


def Fix_Show(df, var_type, unit, measure, groupby_method):
    df.creationDate = pd.to_datetime(df.creationDate)
    df.creationDate = df.creationDate.dt.date
    df.reset_index(inplace=True, drop=True)
    if measure == 'float':
        df.value = df.value.astype(float)
    elif measure == 'int':
        df.value = df.value.astype(int)
    # df.drop(['sourceName', 'unit', 'startDate', 'endDate',
    #         'sourceVersion', 'device'], axis=1, inplace=True)
    # df.reset_index(inplace=True, drop=True)

    if var_type == '_StepCount':
        df.drop(['sourceName', 'unit', 'creationDate', 'endDate',
                'sourceVersion', 'device'], axis=1, inplace=True)
        df.reset_index(inplace=True, drop=True)
        df1 = pd.DataFrame(df.groupby(by='startDate')['value'].sum())
        df1['type'] = type_stem+var_type
        df1['unit'] = unit
        df1.reset_index(inplace=True, drop=False)
        df1 = df1.rename(columns={'startDate': 'date'})
        st.write(df1)
    else:
        df.drop(['sourceName', 'unit', 'startDate', 'endDate',
                'sourceVersion', 'device'], axis=1, inplace=True)
        df.reset_index(inplace=True, drop=True)

        if groupby_method == 'mean':
            df1 = pd.DataFrame(df.groupby(by="creationDate")['value'].mean())
        elif groupby_method == 'sum':
            df1 = pd.DataFrame(df.groupby(by="creationDate")['value'].sum())
        df1['type'] = type_stem+var_type
        df1['unit'] = unit
        df1.reset_index(inplace=True, drop=False)
        df1 = df1.rename(columns={'creationDate': 'date'})
    # st.write('after groupby', type(df1), df1)
    return df1


def Fix_VitC(df):
    df.creationDate = pd.to_datetime(df.creationDate)
    df.creationDate = df.creationDate.dt.date
    df.value = df.value.astype(float)
    st.write('original', df)
    df.drop(['sourceName', 'unit', 'startDate', 'endDate',
            'sourceVersion', 'device'], axis=1, inplace=True)
    st.write('after drop', df)
    st.write(type(df.loc[0, 'creationDate']), type(df.loc[0, 'value']))
    df1 = pd.DataFrame(df.groupby(by="creationDate")['value'].sum())
    df1['type'] = type_stem+'DeitaryVitaminC'
    df1['unit'] = 'mg'
    df1.reset_index(inplace=True, drop=False)
    st.write('after groupby', type(df1), df1)
    return df1


def Show_Files():
    show_file = st.sidebar.selectbox(f'Pick one of {len(files)} file to examine', files, index=0)
    a = st.empty()
    df = pd.read_csv(f'{data_path}{show_file}.csv')
    if df.shape[0] == 0:
        a.write('This subset has no data. Please choose another.')
    else:
        a.write(
            f'This subset is {df.shape[0]} rows long. It should take me {df.shape[0]/100} seconds to produce your graph...')
        df.value = df.value.astype(float)
        df.value = df.value.astype(float)
        df.reset_index(inplace=True, drop=True)
        df.sort_values('creationDate', inplace=True)
        _type = df.loc[0, 'type'][24:]
        unit = df.loc[0, 'unit']
        # set sliders for y scale
        y_scale_min = df.value.min()
        y_scale_max = df.value.max()
        y_min = st.sidebar.slider('Pick a min for the Y axis',
                                  min_value=y_scale_min, max_value=y_scale_max, value=y_scale_min)
        y_max = st.sidebar.slider('Pick a max for the Y axis',
                                  min_value=y_scale_min, max_value=y_scale_max, value=y_scale_max)
        df = df[(df.value > y_min) & (df.value < y_max)]
        length = df.shape[0]
        fig, ax = plt.subplots(figsize=(15, 8))

        first_date = df.creationDate.min()
        last_date = df.creationDate.max()
        st.write(first_date, last_date)
        X_df = pd.DataFrame(pd.date_range(first_date, last_date, freq='d'), columns=['date'])

        X_df['trash'] = 0

        df = df.rename(columns={'creationDate': 'date'})

        X_df.date = pd.to_datetime(X_df.date)
        df.date = pd.to_datetime(df.date)
        X_df.set_index('date', drop=True, inplace=True)
        df.set_index('date', drop=True, inplace=True)
        st.write(X_df)
        st.write(df)
        plot_merge_X = pd.merge(X_df, df, right_index=True, left_index=True, how='outer')
        plot_merge_X.reset_index(inplace=True, drop=False)
        st.write(plot_merge_X)

        plt.title(f'{length} Points of Data on {_type} Over Time',
                  fontdict={'fontsize': 24, 'fontweight': 10})
        ax.set_ylabel(unit, fontdict={'fontsize': 20, 'fontweight': 10})
        plt.xticks(rotation=70)
        # plt.plot(df.creationDate, df.value)
        plt.plot(plot_merge_X.date, plot_merge_X.value)
        st.pyplot(fig)
        a.empty()


def Get_Files():
    files = os.listdir('./apple_watch_data')
    files = sorted([x[:-4] for x in files])
    return files


def Fix_HeartRate(df):
    df.creationDate = pd.to_datetime(df.creationDate)
    df.creationDate = df.creationDate.dt.date
    df.reset_index(inplace=True, drop=True)
    df.value = df.value.astype(float)
    st.write('original', df)
    df.drop(['sourceName', 'unit', 'startDate', 'endDate',
            'sourceVersion', 'device'], axis=1, inplace=True)
    st.write('after drop', df)
    df.reset_index(inplace=True, drop=True)
    st.write(type(df.loc[0, 'creationDate']), type(df.loc[0, 'value']))
    df1 = pd.DataFrame(df.groupby(by="creationDate")['value'].mean())
    df1['type'] = type_stem+'HeartRate'
    df1['unit'] = 'count'
    df1.reset_index(inplace=True, drop=False)
    st.write('after groupby', type(df1), df1)
    return df1


def Fix_HRV(df):
    df.creationDate = pd.to_datetime(df.creationDate)
    df.creationDate = df.creationDate.dt.date
    df.value = df.value.astype(float)
    st.write('original', df)
    df.drop(['sourceName', 'unit', 'startDate', 'endDate',
            'sourceVersion', 'device'], axis=1, inplace=True)
    st.write('after drop', df)
    df.reset_index(inplace=True, drop=True)
    st.write(type(df.loc[0, 'creationDate']), type(df.loc[0, 'value']))
    df1 = pd.DataFrame(df.groupby(by="creationDate")['value'].sum())
    df1['type'] = type_stem+'HeartRateVariabilitySDNN'
    df1['unit'] = 'ms'
    df1.reset_index(inplace=True, drop=False)
    st.write('after groupby', type(df1), df1)
    return df1


def Fix_Glucose(df):
    df.creationDate = pd.to_datetime(df.creationDate)
    df.creationDate = df.creationDate.dt.date
    df.value = df.value.astype(int)
    st.write('original', df)
    df.drop(['sourceName', 'unit', 'startDate', 'endDate',
            'sourceVersion', 'device'], axis=1, inplace=True)
    st.write('after drop', df)
    st.write(type(df.loc[0, 'creationDate']), type(df.loc[0, 'value']))
    df1 = pd.DataFrame(df.groupby(by="creationDate")['value'].mean())
    df1['type'] = type_stem+'BloodGlucose'
    df1['unit'] = 'mg/dl'
    df1.reset_index(inplace=True, drop=False)
    st.write('after groupby', type(df1), df1)
    return df1


def Read_Replace(type):
    replace_list = replace_dict.get(type)
    unit, measure, groupby_method = replace_list[0], replace_list[1], replace_list[2]
    return unit, measure, groupby_method


# files = ['DietarySugar', 'BodyMass', 'DietaryVitaminC',
#          'BloodGlucose', 'MindfulSession', 'AppleWalkingSteadiness',
#          'HeartRateVariabilitySDNN', 'HeartRate', 'RestingHeartRate',
#          'FlightsClimbed', 'DietarySodium', 'LeanBodyMass',
#          'WalkingSpeed', 'DietaryFatTotal', 'WalkingDoubleSupportPercentage',
#          'Height', 'DistanceWalkingRunning', 'VO2Max', 'AudioExposureEvent',
#          'WalkingAsymmetryPercentage', 'DietaryPotassium', 'BloodPressureSystolic',
#          'DietaryCarbohydrates', 'AppleExerciseTime', 'WalkingHeartRateAverage',
#          'AppleStandHour', 'BodyMassIndex', 'DietaryEnergyConsumed',
#          'DietaryCholesterol', 'EnvironmentalAudioExposure', 'SleepAnalysis',
#          'DietaryCalcium', 'AppleStandTime', 'DietaryFatPolyunsaturated',
#          'ActiveEnergyBurned', 'DietaryProtein', 'DietaryIron',
#          'BloodPressureDiastolic', 'DietaryFiber', 'RespiratoryRate',
#          'DietaryFatMonounsaturated', 'StepCount', 'SixMinuteWalkTestDistance',
#          'WalkingStepLength', 'BodyFatPercentage', 'BasalEnergyBurned',
#          'HeadphoneAudioExposureEvent', 'HeadphoneAudioExposure', 'DietaryFatSaturated']
replace_dict = {'AppleWalkingSteadiness': ['%', 'float', 'mean'], 'WalkingSpeed': ['mi/hr', 'float', 'mean'],
                'BloodPressureSystolic': ['mmHg', 'int', 'mean'], 'WalkingAsymmetryPercentage': ['%', 'float', 'mean'],
                'WalkingStepLength': ['in', 'float', 'mean'], 'SixMinuteWalkTestDistance': ['m', 'int', 'mean'],
                'AppleExerciseTime': ['min', 'int', 'sum'], 'HeartRate': ['count/min', 'int', 'mean'],
                'DietaryFiber': ['g', 'float', 'sum'], 'BloodPressureDiastolic': ['mmHg', 'int', 'mean'],
                'FlightsClimbed': ['count', 'int', 'sum'], 'DietaryCalcium': ['mg', 'float', 'sum'],
                'WalkingDoubleSupportPercentage': ['%', 'float', 'mean'], 'Height': ['ft', 'float', 'mean'],
                'BloodGlucose': ['mg/dL', 'int', 'mean'], 'DietaryCarbohydrates': ['g', 'float', 'sum'],
                'WalkingHeartRateAverage': ['count/min', 'float', 'mean'], 'DietarySugar': ['g', 'float', 'sum'],
                'BodyFatPercentage': ['%', 'float', 'mean'], 'DietaryFatPolyunsaturated': ['g', 'float', 'sum'],
                'DietaryCholesterol': ['mg', 'float', 'sum'], 'EnvironmentalAudioExposure': ['dBASPL', 'float', 'mean'],
                'AppleStandTime': ['min', 'int', 'sum'], 'DistanceWalkingRunning': ['mi', 'float', 'sum'],
                'VO2Max': ['mL/min·kg', 'float', 'mean'], 'DietaryFatMonounsaturated': ['g', 'float', 'sum'],
                'DietaryIron': ['mg', 'float', 'sum'], 'RespiratoryRate': ['count/min', 'float', 'mean'],
                'BodyMass': ['lb', 'float', 'mean'], 'DietaryFatSaturated': ['g', 'float', 'mean'],
                'HeadphoneAudioExposure': ['dBASPL', 'float', 'mean'], 'BasalEnergyBurned': ['Cal', 'int', 'sum'],
                'RestingHeartRate': ['count/min', 'int', 'mean'], 'DietaryProtein': ['g', 'float', 'sum'],
                'BodyMassIndex': ['count', 'float', 'mean'], 'DietarySodium': ['mg', 'float', 'sum'],
                'DietaryFatTotal': ['g', 'float', 'sum'], 'ActiveEnergyBurned': ['Cal', 'int', 'sum'],
                'StepCount': ['count', 'int', 'sum'], 'DietaryEnergyConsumed': ['Cal', 'float', 'sum'],
                'HeartRateVariabilitySDNN': ['ms', 'float', 'mean'], 'DietaryVitaminC': ['mg', 'float', 'sum'],
                'LeanBodyMass': ['lb', 'float', 'mean'], 'DietaryPotassium': ['mg', 'float', 'sum']}
read_path = 'apple_health_export/export.xml'
data_path = './apple_watch_data/'
type_stem = 'HKQuantityTypeIdentifier'
