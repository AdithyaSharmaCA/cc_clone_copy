import requests

def check_rabbitmq_health():
    rabbitmq_url = 'http://localhost:15672/api/healthchecks/node'
    rabbitmq_user = 'guest'
    rabbitmq_pass = 'guest'

    try:
        response = requests.get(rabbitmq_url, auth=(rabbitmq_user, rabbitmq_pass))
        response.raise_for_status()
        health_data = response.json()
        
        # Check if RabbitMQ node is running
        if health_data['status'] == 'ok':
            return True, 'RabbitMQ server is running and healthy'
        else:
            return False, 'RabbitMQ server is not healthy'

    except requests.RequestException as e:
        return False, f'Failed to connect to RabbitMQ server: {e}'

if __name__ == "__main__":
    is_healthy, message = check_rabbitmq_health()
    if is_healthy:
        print("RabbitMQ is healthy")
    else:
        print(f"RabbitMQ is not healthy: {message}")
