import json

def response(dialog_action_type, intent_name, intent_slots=None, message=None, slot_to_elicit=None):
    res = {
        'sessionState': {
            'dialogAction': {
                'type': dialog_action_type
            },
            'intent': {
                'name': intent_name,
                'slots': intent_slots,
                'state': 'Fulfilled' if dialog_action_type == 'Close' else 'InProgress'
            }
        }
    }

    if dialog_action_type == 'ElicitSlot':
        res['sessionState']['dialogAction']['slotToElicit'] = slot_to_elicit

    if message:
        res['messages'] = [{'contentType': 'PlainText', 'content': message}]

    return res

def greeting_intent_handler(intent_name):
    return response('Close', intent_name, message='Hello! How can I help you?')

def thank_you_intent_handler(intent_name):
    return response('Close', intent_name, message="You're welcome!")

def dining_suggestions_intent_handler(intent_name, intent_slots):
    location = intent_slots.get('Location')
    cuisine = intent_slots.get('Cuisine')
    party_size = intent_slots.get('PartySize')
    dining_time = intent_slots.get('DiningTime')
    email = intent_slots.get('Email')

    # Initial prompt for `Location`
    if not location:
        return response('Delegate', intent_name, intent_slots)

    # Custom validation for `Location`
    location = location.get('value')
    if location.get('originalValue') and not location.get('interpretedValue'):
        return response('ElicitSlot', intent_name, intent_slots, 'Please enter a valid city.', 'Location')

    # Initial prompt for `Cuisine`
    if not cuisine:
        return response('Delegate', intent_name, intent_slots)

    # # This doesn't trigger (lex doesn't set value for invalid input to custom slot type)
    cuisine = cuisine.get('value')
    # if cuisine.get('originalValue') and not cuisine.get('interpretedValue'):
    #     return response('ElicitSlot', intent_name, intent_slots, 'Please enter a valid cuisine.', 'Cuisine')

    # Initial prompt for `PartySize`
    if not party_size or not party_size.get('value'):
        return response('Delegate', intent_name, intent_slots)

    # Custom validation for `PartySize`
    party_size = party_size.get('value')
    if (
        not party_size.get('interpretedValue')
        or float(party_size.get('interpretedValue')) != int(float(party_size.get('interpretedValue')))  # must be whole number
        or int(party_size.get('interpretedValue')) <= 0 # must be greater than 0
    ):
        return response('ElicitSlot', intent_name, intent_slots, 'Please enter a valid number of people.', 'PartySize')

    # Initial prompt for `DiningTime`
    if not dining_time:
        return response('Delegate', intent_name, intent_slots)

    # Custom validation for `DiningTime`
    dining_time = dining_time.get('value')
    if dining_time.get('originalValue') and not dining_time.get('interpretedValue'):
        return response('ElicitSlot', intent_name, intent_slots, 'Please enter a valid time.', 'DiningTime')

    # Initial prompt for `Email`
    if not email:
        return response('Delegate', intent_name, intent_slots)

    # Custom validation for `Email`
    email = email.get('value')
    if email.get('originalValue') and not email.get('interpretedValue'):
        return response('ElicitSlot', intent_name, intent_slots, 'Please enter a valid email.', 'Email')
    

    message = "You're all set! Expect restaurant suggestions in your email shortly."

    # Final fulfillment
    return response('Close', intent_name, intent_slots, message)

def fallback_intent_handler(intent_name):
    return response('Close', intent_name, message="Sorry, I don't understand that request.")

def lambda_handler(event, context):
    intent_name = event['sessionState']['intent']['name']
    intent_slots = event['sessionState']['intent'].get('slots', {})

    if intent_name == 'GreetingIntent':
        return greeting_intent_handler(intent_name)

    if intent_name == 'ThankYouIntent':
        return thank_you_intent_handler(intent_name)

    if intent_name == 'DiningSuggestionsIntent':
        return dining_suggestions_intent_handler(intent_name, intent_slots)

    if intent_name == 'FallbackIntent':
        return fallback_intent_handler(intent_name)

# Testing
if __name__ == '__main__':
    event = {
        'sessionState': {
            'intent': {
                'name': 'DiningSuggestionsIntent',
                'slots': {
                    'Location': {'value': {'interpretedValue': 'New York'}},
                    'Cuisine': {'value': {'interpretedValue': 'Italian'}},
                    'PartySize': {'value': {'interpretedValue': '2'}},
                    'DiningTime': {'value': {'interpretedValue': '7:00 PM'}},
                    'Email': {'value': {'interpretedValue': 'user@example.com'}}
                }
            }
        }
    }
    response = lambda_handler(event, None)
    print('Response:', json.dumps(response))