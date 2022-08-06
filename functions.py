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
        os.path.mkdir('./apple_watch_data')
        st.write('I am setting up your data. This will take a few minutes.')
        selector_index = 0
    function = st.sidebar.selectbox(
        'Choose a function', ['reset database', 'examine a subset'], index=selector_index)
    if function == 'reset database':
        Reset_Database()
    elif function == 'examine a subset':
        Show_Files()


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
write_path = './apple_watch_data/'
