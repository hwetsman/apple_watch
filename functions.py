import pandas as pd
import streamlit as st
import xml.etree.ElementTree as ET


@st.cache()
def Get_Data(path_to_watch_data):
    tree = ET.parse(path_to_watch_data)
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]
    df = pd.DataFrame(record_list)
    return df


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
