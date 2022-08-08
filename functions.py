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
    df = Get_Data('apple_health_export/export.xml')
    # create datetime cols
    for col in ['creationDate', 'startDate', 'endDate']:
        df[col] = pd.to_datetime(df[col])
    types = [x[24:] for x in list(set(df.type.tolist()))]
    for type in types:
        filter = type_stem+type
        df1 = df[df.type == filter]
        if type == 'BloodGlucose':
            df1 = Fix_Glucose(df1)
        elif type == 'FlightsClimbed':
            df1 = Fix_Flights(df1)
        elif type == 'HeartRateVariabilitySDNN':
            df1 = Fix_HRV(df1)
        elif type == 'DietarySugar':
            df1 = FixSugar(df1)
        df1.to_csv(f'{data_path}{type}.csv', index=False)
        st.write(f'I have written the file {type}.csv')


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
    df = pd.read_csv(f'{data_path}{show_file}.csv')
    a = st.empty()
    a.write(
        f'This subset is {df.shape[0]} rows long. It should take me {df.shape[0]/100} seconds to produce your graph...')
    df.value = df.value.astype(float)
    df.value = df.value.astype(float)
    df.reset_index(inplace=True, drop=True)
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
    st.write(y_scale_min, type(y_scale_min), y_scale_max, type(y_scale_max))
    st.write(df)

    length = df.shape[0]

    fig, ax = plt.subplots(figsize=(15, 8))
    plt.title(f'{length} Points of Data on {_type} Over Time',
              fontdict={'fontsize': 24, 'fontweight': 10})
    ax.set_ylabel(unit, fontdict={'fontsize': 20, 'fontweight': 10})
    plt.xticks(rotation=70)
    plt.plot(df.creationDate, df.value)
    st.pyplot(fig)
    a.empty()


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


files = ['DietarySugar', 'BodyMass', 'DietaryVitaminC',
         'BloodGlucose', 'MindfulSession', 'AppleWalkingSteadiness',
         'HeartRateVariabilitySDNN', 'HeartRate', 'RestingHeartRate',
         'FlightsClimbed', 'DietarySodium', 'LeanBodyMass',
         'WalkingSpeed', 'DietaryFatTotal', 'WalkingDoubleSupportPercentage',
         'Height', 'DistanceWalkingRunning', 'VO2Max', 'AudioExposureEvent',
         'WalkingAsymmetryPercentage', 'DietaryPotassium', 'BloodPressureSystolic',
         'DietaryCarbohydrates', 'AppleExerciseTime', 'WalkingHeartRateAverage',
         'AppleStandHour', 'BodyMassIndex', 'DietaryEnergyConsumed',
         'DietaryCholesterol', 'EnvironmentalAudioExposure', 'SleepAnalysis',
         'DietaryCalcium', 'AppleStandTime', 'DietaryFatPolyunsaturated',
         'ActiveEnergyBurned', 'DietaryProtein', 'DietaryIron',
         'BloodPressureDiastolic', 'DietaryFiber', 'RespiratoryRate',
         'DietaryFatMonounsaturated', 'StepCount', 'SixMinuteWalkTestDistance',
         'WalkingStepLength', 'BodyFatPercentage', 'BasalEnergyBurned',
         'HeadphoneAudioExposureEvent', 'HeadphoneAudioExposure', 'DietaryFatSaturated']
read_path = 'apple_health_export/export.xml'
data_path = './apple_watch_data/'
type_stem = 'HKQuantityTypeIdentifier'
