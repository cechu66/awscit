#!/usr/local/bin/python3
import boto3
import csv

#using for Compute Optimizer

def get_compute_optimizer_report(profile):
    session = boto3.Session(profile_name=profile)
    client = session.client('compute-optimizer')

    response = client.get_ebs_volume_recommendations(maxResults=100)
    recommendations = response['volumeRecommendations']


    with open('compute_optimizer_report.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['VolumeArn', 'Finding', 'CurrentConfiguration', 'RecommendedConfiguration'])

        for recommendation in recommendations:
            volume_arn = recommendation['volumeArn']
            finding = recommendation['finding']
            current_configuration = recommendation['currentConfiguration']
            recommended_configuration = recommendation.get('volumeRecommendationOptions', [{}])[0].get('configuration')
            
            writer.writerow([volume_arn, finding, current_configuration, recommended_configuration])

def get_ec2_instance_recommendations(profile):
    session = boto3.Session(profile_name=profile)
    client = session.client('compute-optimizer')

    # Get EC2 instance recommendations
    response = client.get_ec2_instance_recommendations(maxResults=100)
    recommendations = response['instanceRecommendations']

    with open('ec2_instance_recommendations.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['InstanceArn', 'Finding', 'CurrentInstanceType', 'RecommendedInstanceType'])

        for recommendation in recommendations:
            instance_arn = recommendation['instanceArn']
            finding = recommendation['finding']
            current_instance_type = recommendation['currentInstanceType']
            recommended_instance_type = recommendation.get('recommendationOptions', [{}])[0].get('instanceType')

            writer.writerow([instance_arn, finding, current_instance_type, recommended_instance_type])
def get_ecs_service_recommendations(profile):
    session = boto3.Session(profile_name=profile)
    client = session.client('compute-optimizer')

    # Get ECS service recommendations
    response = client.get_ecs_service_recommendations(maxResults=100)
    recommendations = response['ecsServiceRecommendations']

    with open('ecs_service_recommendations.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ServiceArn', 'Finding', 'CurrentTaskDefinition', 'RecommendedTaskDefinition'])

        for recommendation in recommendations:
            service_arn = recommendation['serviceArn']
            finding = recommendation['finding']
            current_task_definition = recommendation['currentServiceConfiguration']
            recommended_task_definition = recommendation.get('serviceRecommendationOptions')

            writer.writerow([service_arn, finding, current_task_definition, recommended_task_definition])

if __name__ == "__main__":
    profile = 'input-profile-here'
    get_compute_optimizer_report(profile)
    get_ec2_instance_recommendations(profile)
    get_ecs_service_recommendations(profile)