# Plot My Path
---

[To view site]
[To view backend]
 
## Table of Contents

## [UX](#ux-1)

- [Primary Goals](#primary-goals) 
- [Business Goals](#business-goals)
- [User Goals](#user-goals) 
- [User Stories](#user-stories)
- [Design Choices](#design-choices) 
- [ERD Diagram](#erd-diagram) 
- [Database Architecture](#database-architecture)
- [Wireframes](#wireframes) 

## [Features](#features-1)

- [Existing features](#existing-features) 
- [User Goals mapping](#user-goals-mapping) 
- [Features left to implement](#features-left-to-implement) 
- [User Goals still to implement](#user-goals-still-to-implement) 

## [Technologies used](#technologies-used-1)

## [Testing](#testing-1)

- [Lighthouse tests](#lighthouse-tests) 
- [HTML tests](#html-tests) 
- [CSS tests](#css-tests) 
- [Python code validation](#python-code-validation)
- [JSX Testing](#jsx-testing)
- [API Testing](#api-testing) 
- [Security](#security) 
- [Automated Testing](#automated-testing) 
- [Contrast tests](#contrast-tests) 
- [Keyboard Accessibility tests](#keyboard-accessibility-tests) 
- [Manual Features and Usability Testing Log](#manual-features-and-usability-testing-log) 
- [Development bugs and fixes](#development-bugs-and-fixes) 
- [Cross browser testing](#cross-browser-testing) 
- [User Testing](#user-testing) 

## [Deployment](#deployment-1) 

- [How to run this project](#how-to-run-this-project) 

## [Credits](#credits-1) 

- [Content/Media/Code/Acknowledgements](#contentmediacodeacknowledgements) 
- [dependencies](#dependencies) 

### UX
---
#### Primary Goals
---

The primary goals of Plot My Path are:

- To simplify planning a trip by taking users from a destination idea to a day-by-day itinerary in one guided flow.
- To provide a wide selection of destinations and attractions that users can browse and search.
- To personalise trips around each user's travel style and interests.
- To bring practical information such as costs, opening times and weather together in one place.
- To get users trying destinations and attractions they may not have considered before.

[Back to top](#plot-my-path) 
#### Business Goals
---

The business goals of Plot My Path are:

- To let users experience the app with a free first trip before they are asked to pay.
- To convert free users into premium members through a one-off £5 payment that unlocks unlimited trips.
- To build trust by handling payments securely through Stripe and offering a fair refund policy (within 14 days and no more than 3 trips created since purchase).
- To keep accounts genuine by requiring email verification before a user can sign in.
- To keep running costs low by serving images from Cloudinary and using a third-party service for weather data.
- To give users an easy way to get help through a contact form.
- Long term business goals include recommending attractions to users based on their saved travel preferences.

[back to top](#plot-my-path)
#### User Goals
---

The goals for users would be:

- Save time researching and organising a trip by having everything in one place.
- Plan realistic days using attraction opening times, visit lengths and the weather forecast.
- Find inspiration from new destinations and attractions.
- Keep a shortlist of favourite destinations to come back to.
- Pay once rather than commit to a subscription, with the option of a refund if premium isn't right for them.
- Know that their trips and personal details are private.

[back to top](#plot-my-path)
#### User Stories
---

Acceptance criteria are listed beneath each user story.

**Accounts and onboarding**

- As a new visitor, I can create an account with my name, email and password so that I can save and manage my own trips.
  - First name and last name are required.
  - After signing up I am told to check my inbox to verify my email.
  - I cannot sign in until my email address has been verified.

- As a visitor, I can view a landing page and an onboarding carousel so that I understand what the app does before I sign up.
  - Both pages can be viewed without signing in.

- As a signed-in user, I can see a personalised homepage so that I feel welcomed and get ideas straight away.
  - The greeting changes between morning, afternoon and evening.
  - A selection of featured destinations is shown.

- As a signed-in user, I can view my profile page so that I can see my account and membership in one place.
  - Messages about my membership and refunds appear here.

**Discovering destinations**

- As a signed-in user, I can browse destinations by continent so that I can narrow down where I want to go.
  - All destinations are shown by default.
  - Choosing a continent filters the list.

- As a signed-in user, I can search destinations by name so that I can find a place quickly.
  - Partial matches are returned, up to a maximum of 10.
  - An empty search returns no results.

- As a signed-in user, I can view a destination's details so that I can decide whether it suits me.
  - The page shows the description, average cost per day, image and attractions.
  - It shows whether I have already saved the destination.

- As a signed-in user, I can see an attraction's category, visit length, entry cost, rating and opening times so that I can plan realistic days.

- As a signed-in user, I can save and unsave destinations so that I can build a shortlist for later.
  - The same destination cannot be saved twice.
  - The heart/favourite state updates without reloading the page.

- As a signed-in user, I can view my saved destinations so that I can quickly return to the places I liked.
  - Only my own saved destinations are shown.

**Creating a trip**

- As a signed-in user, I can create a trip through a step-by-step form so that setting up a trip feels simple.
  - The steps are preferences, destination and name, dates and budget, and a final review.
  - When I finish I am taken straight to my itinerary.

- As a signed-in user, I can set my travel style and interests so that my trips reflect what I enjoy.
  - My preferences are saved to my profile and loaded into the itinerary builder.

- As a signed-in user, I can only enter sensible dates so that I don't create an impossible trip.
  - The start date cannot be in the past.
  - The end date cannot be before the start date.
  - A trip must be at least one day long.

- As a free user, I am told when I have used my free trip so that I understand how to create more.
  - After one trip I am redirected to my profile with a message about upgrading.
  - The limit is checked again when the form is submitted.
  - Premium members and staff are not limited.

- As a signed-in user, I can view all of my trips so that I can pick up where I left off.
  - Trips are listed with the most recent start date first.
  - Only my own trips are shown.

- As a signed-in user, I can delete a trip so that I can remove plans I no longer need.
  - Only my own trips can be deleted.
  - A confirmation message is shown.

**Building an itinerary**

- As a signed-in user, I can see a day for every date of my trip so that I can plan one day at a time.
  - Days are numbered from 1 and created automatically.
  - Reopening the itinerary never creates duplicate days.

- As a signed-in user, I can add an attraction to a day with a start and end time so that I can build a realistic plan.
  - The attraction must belong to the trip's destination.
  - The start time must be before the end time.
  - Invalid or missing information returns a clear error.

- As a signed-in user, I can remove an activity from a day so that I can change my plans.
  - The remaining activities are renumbered with no gaps.

- As a signed-in user, I can see the weather forecast for my trip dates so that I can plan around it.
  - Daily temperatures, conditions and chance of rain are shown.
  - If the weather service is unavailable, a message is shown and the itinerary still loads.

- As a signed-in user, I can be confident that other people cannot see or change my trips so that my plans stay private.
  - Requesting another user's trip returns "not found".

**Premium membership and payments**

- As a free user, I can pay a one-off £5 to become a premium member so that I can create unlimited trips.
  - Payment is taken through Stripe Checkout.
  - If I am already a premium member I am redirected and cannot pay twice.

- As a user who has paid, I can have my membership activated reliably so that I get what I paid for.
  - The success page checks that the payment belongs to me and has been completed.
  - A Stripe webhook also activates the membership as a backup.
  - Duplicate callbacks do not create duplicate payments.

- As a user whose payment fails, I can see a clear message so that I know what happened and can try again.

- As a premium member, I can request a refund so that I am protected if premium isn't right for me.
  - Refunds are available within 14 days of purchase and when no more than 3 trips have been created since.
  - Premium access is removed and the payment is marked as refunded.
  - Refunds made from the Stripe dashboard also remove premium access.

**Recommendations and support**

- As a signed-in user, I can receive recommended attractions for my trip based on my preferences so that I can discover things I'd enjoy. *(planned feature)*
  - Each recommendation has a score and a short reason.
  - The highest scoring recommendations are shown first.

- As a visitor or signed-in user, I can contact the team through a form so that I can get help.
  - Name, email, subject and message are required.
  - If I am signed in, my name and email are filled in for me.
  - The team receives my message by email and can reply directly to me.

[back to top](#plot-my-path)
#### Design Choices
---

Plot My Path is a mobile-first travel planning app. Its interface helps users discover destinations, create trips, organise activities and make decisions while travelling.

The design uses a clean, modern style with rounded cards, generous spacing, clear typography, imagery and a purple and blue colour scheme. These choices make the app feel approachable and easy to navigate, while keeping travel information the main focus.

The layout adapts progressively to larger screens rather than creating separate mobile, tablet and desktop experiences. On small screens, information is prioritised and shown one step at a time. On larger screens, related information can appear side by side, making better use of the space.

This suits a travel app because people use it in different contexts: planning at home on a desktop, researching destinations on a tablet, or checking an itinerary on a phone while travelling.

[back to top](#plot-my-path)
#### ERD Diagram
---

<details>
<summary> ERD Data flow  </summary>


 | Model       	| Relationship      	| Model               	|
|-------------	|-------------------	|---------------------	|
| User        	| has               	| Travel_Preference   	|
| User        	| Saves             	| Saved_Destination   	|
| User        	| creates           	| Trip                	|
| User        	| makes             	| Payment             	|
| User        	| holds             	| Prermium_Membership 	|
| User        	| recieves          	| Recommendation      	|
| Payment     	| activates         	| Premium_Membership  	|
|             	|                   	|                     	|
| Country     	| contains          	| Destination         	|
| Destination 	| has               	| Attraction          	|
| Destination 	| saved as          	| Saved_Destination   	|
| Destination 	| is visited in     	| Trip                	|
|             	|                   	|                     	|
| Trip        	| is split into     	| Trip_Day            	|
| Trip        	| generates         	| Recommendation      	|
| Trip Day    	| schedules         	| Planned_activity    	|
| Attraction  	| is scheduled as   	| Planned_Activity    	|
| Attraction  	| is recommended in 	| Recommendation      	|
</details>

<details>
<summary> ERD Diagram  </summary>

![ERD diagram](/static/images/readme-img/pmp-erd.png)
</details>

[back to top](#plot-my-path)
#### Database Architecture
---

<details>
<summary> Database Architecture </summary>

The backend application uses a relational database structure built with Django. Below is a description of the database entities shown in the ERD diagram above. The User model is provided by Django and django-allauth, so it is not described here.

###### TravelPreference Model

- user: A ForeignKey linking the preferences to the user's account, using models.CASCADE so they are removed if the user is deleted.
- travel_style: A CharField with a 50-character limit, restricted to a set of choices (adventure, relaxation, city break, culture, food & drink and nature).
- walking_preference, culture, food, nature, history, nightlife, family_friendly, solo_travel: BooleanFields that record the user's interests, each defaulting to False.

###### SavedDestination Model

- user: A ForeignKey linking the saved item to a user, with the related name saved_destinations and cascading deletes.
- destination: A ForeignKey linking the saved item to a Destination, with the related name saved_by_users and cascading deletes.
- created_at: A DateTimeField that records when the destination was saved, set automatically.
- Meta: A unique_together constraint on user and destination to stop the same destination being saved twice.

###### Country Model

- name: A CharField with a 100-character limit that stores the country name and is used as the natural key when loading fixtures.
- code: A CharField with a 3-character limit that stores the ISO country code.
- continent: A CharField with a 50-character limit that is used to filter destinations.

###### Destination Model

- country: A ForeignKey to the Country model with the related name destinations and cascading deletes.
- name: A CharField with a 100-character limit.
- slug: A unique SlugField used as the natural key for fixtures and to build the Cloudinary image address.
- description: A TextField holding the destination description.
- latitude and longitude: DecimalFields (9 digits, 6 decimal places) used for weather lookups.
- average_cost_per_day: A DecimalField (10 digits, 2 decimal places) storing the estimated daily cost.
- get_image_url: A property that builds the Cloudinary image address from the slug so images do not need to be stored in the database.

###### Attraction Model

- destination: A ForeignKey to the Destination model with the related name attractions and cascading deletes.
- name, slug, description: Fields storing the attraction name, its slug and a full description.
- category: A CharField with a 50-character limit.
- latitude and longitude: DecimalFields (9 digits, 6 decimal places) storing the attraction's location.
- average_visit_minutes: An IntegerField storing how long a visit usually takes.
- entry_cost: A DecimalField (10 digits, 2 decimal places) storing the entry price.
- rating: An optional DecimalField (3 digits, 2 decimal places) which can be left blank or null.
- opening_time and closing_time: TimeFields storing when the attraction is open.
- Meta: A unique_together constraint on destination and slug.
- get_image_url: A property that builds the Cloudinary image address from the slug.

###### Trip Model

- user: A ForeignKey to the user who owns the trip, with the related name trips and cascading deletes.
- destination: A ForeignKey to the Destination model with the related name trips and cascading deletes.
- name: A CharField with a 150-character limit.
- start_date and end_date: DateFields storing the trip dates.
- budget: A DecimalField (10 digits, 2 decimal places) storing the user's budget.
- created_at and updated_at: DateTimeFields set automatically when the trip is created and updated.

###### TripDay Model

- trip: A ForeignKey to the Trip model with the related name trip_days and cascading deletes.
- date: A DateField storing the calendar date of the day.
- day_number: An IntegerField storing the day's position within the trip.
- notes: An optional TextField for the user's notes.

###### PlannedActivity Model

- trip_day: A ForeignKey to the TripDay model with the related name planned_activities and cascading deletes.
- attraction: A ForeignKey to the Attraction model with the related name planned_activities and cascading deletes.
- start_time and end_time: TimeFields storing when the activity takes place.
- order: An IntegerField that sets the position of the activity within the day.
- notes: An optional TextField for the user's notes.
- status: A CharField with a 50-character limit, defaulting to "scheduled".
- Meta: Orders activities by the order field.

###### Recommendation Model

- user: A ForeignKey to the user receiving the recommendation, with the related name recommendations and cascading deletes.
- trip: A ForeignKey to the Trip model with the related name recommendations and cascading deletes.
- attraction: A ForeignKey to the Attraction model with the related name recommendations and cascading deletes.
- score: A DecimalField (5 digits, 2 decimal places) showing how well the attraction matches the user's preferences.
- reason: A TextField limited to 200 characters explaining why the attraction was recommended.
- created_at: A DateTimeField set automatically when the recommendation is created.
- Meta: Orders recommendations from the highest score to the lowest.

###### Payment Model

- user: A ForeignKey to the user who paid, with the related name payments and cascading deletes.
- stripe_payment_id: An optional, unique CharField (255 characters) storing the Stripe payment ID, which also stops the same payment being recorded twice.
- amount: A PositiveIntegerField storing the amount in pence.
- currency: A CharField with a 3-character limit, defaulting to "gbp".
- status: A CharField restricted to pending, succeeded, failed or refunded, defaulting to pending.
- created_at: A DateTimeField set automatically when the payment is recorded.
- amount_pounds: A property that converts the stored pence amount into pounds.

###### PremiumMembership Model

- user: A OneToOneField to the user with the related name membership, so each user can only have one membership.
- payment: An optional OneToOneField to the Payment model that uses models.SET_NULL so the membership remains if the payment record is removed.
- status: A CharField restricted to active, inactive, cancelled, expired or past due, defaulting to inactive.
- stripe_customer_id: An optional, unique CharField (255 characters) storing the Stripe customer ID.
- started_at: An optional DateTimeField recording when premium access began, which is used to work out refund eligibility.
- created_at: A DateTimeField set automatically when the membership record is created.
- is_active: A property that returns True when the status is active.

</details>

[back to top](#plot-my-path)
#### Wireframes 
---
Mobile Wireframes 
---
- Landing page
- ![landing page](/static/images/readme-img/mobile-landing-page.png) 
- Login page
- ![login page](/static/images/readme-img/mobile-login-page.png)
- Register page
- ![register page](/static/images/readme-img/mobile-register-page.png)
- onboarding pages
- ![onboarding page](/static/images/readme-img/mobile-onboarding-pages.png)
- Home page
- ![home page](/static/images/readme-img/mobile-homepage.png)
- Explore destination page
- ![explore destination page](/static/images/readme-img/mobile-explore-destination.png)
- Destination detail page
- ![destination detail page](/static/images/readme-img/mobile-destination-detail.png)
- Create plan page
- ![create page](/static/images/readme-img/mobile-create-plan.png)
- Profile page
- ![profile page](/static/images/readme-img/mobile-profile.png)

Tablet Wireframes
--- 
- Note: For landing page, login/register and onboarding pages please see mobile wireframes as the view on tablet will be identical but on a larger scale. 
- Homepage
- ![]
Desktop Wireframes
--- 
- Note:For landing page, login/register and onboarding pages please see mobile wireframes as the view on desktop will be identical but on a larger scale.  
[back to top](#plot-my-path)
 
[back to top](#plot-my-path)
### Features
---
Plot My Paths features will include:


                    

#### Existing features
---
[back to top](#plot-my-path)
#### User Goals mapping
---
[back to top](#plot-my-path)
#### Features left to implement
---
[back to top](#plot-my-path)
#### User Goals still to implement
---
[back to top](#plot-my-path)
### Technologies used
---
[back to top](#plot-my-path)
### Testing
---

#### Lighthouse tests 
---
[back to top](#plot-my-path)
#### HTML tests 
---
[back to top](#plot-my-path)
#### CSS tests 
---
[back to top](#plot-my-path)
#### Python code validation
---


[back to top](#plot-my-path)
#### JSX Testing
---
[back to top](#plot-my-path)
#### API Testing 
---
[back to top](#plot-my-path)
#### Security 
---
[back to top](#plot-my-path)
#### Automated Testing
---

##### Django Testing(Using Djangos testing suite)
---
###### Core Tests-The Tests
---
**core tests ran at commit 173448e**
 **Pages Tests**

- The landing page and onboarding page load for anyone and use their
  expected templates.
- The homepage requires login: a logged-out visitor is redirected.
- The homepage greeting depends on the time of day: "Good morning" at 9am,
  "Good afternoon" at 2pm and "Good evening" at 8pm. The clock is mocked, so
  the tests give the same result whenever they run.

**Contact page**

- The page loads and uses the contact template.
- For a logged-in user the form is pre-filled with their first name and
  email address.
- A valid submission sends one email containing the message and redirects
  back to the contact page.(Using Django's in-memory test mailbox.)
- An invalid submission re-renders the form and sends no email.

**Forms**

**Signup form**
- Valid with a first and last name, and invalid when they are missing.
- Calling signup saves the first and last name onto the user.

**Contact form**
- Valid with a name, email, subject and message.
- Invalid when any field is missing, and invalid for a malformed email
  address.

**results **
- ran using python manage.py test core.tests --keepdb and all tests passed 
----------------------------------------------------------------------
Ran 16 tests in 17.075s

OK
Preserving test database for alias 'default'...
 


[back to top](#plot-my-path)
#### Contrast tests 
---
[back to top](#plot-my-path)
#### Keyboard Accessibility tests 
---
[back to top](#plot-my-path)
#### Manual Features and Usability Testing Log
---
[back to top](#plot-my-path)
#### Development bugs and fixes
---
[back to top](#plot-my-path)
#### Cross browser testing
---
[back to top](#plot-my-path)
#### User Testing 
---
[back to top](#plot-my-path)
### Deployment
---
[back to top](#plot-my-path)
#### How to run this project 
---
[back to top](#plot-my-path)
### Credits
---

[back to top](#plot-my-path)
#### Content/Media/Code/Acknowledgements 
---
[back to top](#plot-my-path)
#### dependencies 
---
[back to top](#plot-my-path)



