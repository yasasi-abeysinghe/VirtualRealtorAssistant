# Virtual Realtor Assistant

Voice-enabled dialogue assistant for finding housing/apartments.


This system,
* Interacts with the user via a voice-enabled interface.
* Performs named entity recognition (NER) using Flair to find user's requirements.
* Finds the housing/apartment matches using real estate data from the Redfin database. (Using Python-redfin is a Python wrapper for Redfin’s API.) 
* Display the matching houses/apartments along with location, price, bedrooms, bathrooms, and year built