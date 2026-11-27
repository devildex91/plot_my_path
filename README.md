# Plot My Path
---

[To view site](https://plot-my-path.onrender.com/)
[To view backend](https://plot-my-path.onrender.com/admin/login/?next=/admin/)
 
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

1. As a new visitor, I can create an account with my name, email and password so that I can save and manage my own trips.
  - First name and last name are required.
  - After signing up I am told to check my inbox to verify my email.
  - I cannot sign in until my email address has been verified.

2. As a visitor, I can view a landing page and information so that I understand what the app does before I sign up.
  - Both pages can be viewed without signing in.

3. As a signed-in user, I can see a personalised homepage so that I feel welcomed and get ideas straight away.
  - The greeting changes between morning, afternoon and evening.
  - A selection of featured destinations is shown.

4. As a signed-in user, I can view my profile page so that I can see my account and membership in one place.
  - Messages about my membership and refunds appear here.

**Discovering destinations**

5. As a signed-in user, I can browse destinations by continent so that I can narrow down where I want to go.
  - All destinations are shown by default.
  - Choosing a continent filters the list.

6. As a signed-in user, I can search destinations by name so that I can find a place quickly.
  - Partial matches are returned, up to a maximum of 10.
  - An empty search returns no results.

7. As a signed-in user, I can view a destination's details so that I can decide whether it suits me.
  - The page shows the description, average cost per day, image and attractions.
  - It shows whether I have already saved the destination.

8. As a signed-in user, I can see an attraction's category, visit length, entry cost, rating and opening times so that I can plan realistic days.

9.  As a signed-in user, I can save and unsave destinations so that I can build a shortlist for later.
  - The same destination cannot be saved twice.
  - The heart/favourite state updates without reloading the page.

10. As a signed-in user, I can view my saved destinations so that I can quickly return to the places I liked.
  - Only my own saved destinations are shown.

**Creating a trip**

11. As a signed-in user, I can create a trip through a step-by-step form so that setting up a trip feels simple.
  - The steps are preferences, destination and name, dates and budget, and a final review.
  - When I finish I am taken straight to my itinerary page

12. As a signed-in user, I can set my travel style and interests so that my trips reflect what I enjoy.
  - My preferences are saved to my profile and loaded into the itinerary builder.

13. As a signed-in user, I can only enter sensible dates so that I don't create an impossible trip.
  - The start date cannot be in the past.
  - The end date cannot be before the start date.
  - A trip must be at least one day long.

14. As a free user, I am told when I have used my free trip so that I understand how to create more.
  - After one trip I am redirected to my profile with a message about upgrading.
  - The limit is checked again when the form is submitted.
  - Premium members and staff are not limited.

15. As a signed-in user, I can view all of my trips so that I can pick up where I left off.
  - Trips are listed with the most recent start date first.
  - Only my own trips are shown.

16. As a signed-in user, I can delete a trip so that I can remove plans I no longer need.
  - Only my own trips can be deleted.
  - A confirmation message is shown.

**Building an itinerary**

17. As a signed-in user, I can see a day for every date of my trip so that I can plan one day at a time.
  - Days are numbered from 1 and created automatically.
  - Reopening the itinerary never creates duplicate days.

18. As a signed-in user, I can add an attraction to a day with a start and end time so that I can build a realistic plan.
  - The attraction must belong to the trip's destination.
  - The start time must be before the end time.
  - Invalid or missing information returns a clear error.

19. As a signed-in user, I can alter or remove an activity from a day so that I can change my plans.
  - The remaining activities are renumbered with no gaps.

20. As a signed-in user, I can see the weather forecast for my trip dates so that I can plan around it.
  - Daily temperatures, conditions and chance of rain are shown.
  - If the weather service is unavailable, a message is shown and the itinerary still loads.

21. As a signed-in user, I can be confident that other people cannot see or change my trips so that my plans stay private.
  - Requesting another user's trip returns "not found".

**Premium membership and payments**

22.  As a free user, I can pay a one-off fee to become a premium member so that I can create unlimited trips.
  - Payment is taken through Stripe Checkout.
  - If I am already a premium member I am redirected and cannot pay twice.

23. As a user who has paid, I can have my membership activated reliably so that I get what I paid for.
  - The success page checks that the payment belongs to me and has been completed.
  - A Stripe webhook also activates the membership as a backup.
  - Duplicate callbacks do not create duplicate payments.

24. As a user whose payment fails, I can see a clear message so that I know what happened and can try again.

25. As a premium member, I can request a refund so that I am protected if premium isn't right for me.
  - Refunds are available within 14 days of purchase and when no more than 3 trips have been created since.
  - Premium access is removed and the payment is marked as refunded.
 

**Recommendations and support**

26. As a signed-in user, I can receive recommended attractions for my trip based on my preferences so that I can discover things I'd enjoy.
  - Each recommendation has a score and a short reason.
  - The highest scoring recommendations are shown first.

27. As a visitor or signed-in user, I can contact the team through a form so that I can get help.
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
#### Existing features
---

##### Trip planning
- **Guided trip creation:** a four-step wizard collects your travel preferences, destination and trip name, dates and budget, then a review step before the trip is created.
- **Travel preferences:** choose a travel style and interests such as culture, food, nature, history, nightlife, family-friendly and solo travel. Your preferences are saved to your profile.
- **Itinerary builder:** every trip gets a day-by-day itinerary generated automatically from its start and end dates.
- **Plan activities:** add attractions from your destination to any day with start and end times, and remove them again. Activities are numbered in order, and the numbering closes up when one is deleted.
- **Weather forecast:** daily forecasts (temperatures, conditions and chance of rain) are shown for your trip dates, powered by Visual Crossing. If the forecast is unavailable, the itinerary still loads.
- **My trips:** view and delete your own trips.

##### Destinations
- **Browse destinations and attractions:** explore destinations, each with its own set of attractions (category, entry cost, typical visit length and opening times).
- **Favourites:** save destinations with a one-click favourite button, without reloading the page.
- **Search:** a live search bar for finding destinations.

##### Accounts and membership
- **Sign up and log in:** email-based accounts, plus sign in with Google.
- **Onboarding:** a short onboarding flow for new users.
- **Free and premium plans:** free accounts can create one trip, and premium members can create as many as they like. Premium upgrades are handled through Stripe Checkout.
- **Profile page** for managing your account and membership.

##### Design and experience
- **Responsive layout:** a bottom navigation bar on mobile that moves to the top on larger screens.
- **Light and dark themes:** a theme toggle (Fantasy and Sunset) that remembers your choice and falls back to your system preference.
- **Flash messages** that fade out automatically.
- **Custom 404 page.**

##### Built with
Django, django-allauth, React, Vite (via django-vite), Tailwind CSS with daisyUI, Cloudinary for images, Stripe for payments, Brevo for email, and WhiteNoise for static files.

[back to top](#plot-my-path)
#### User Goals mapping
---
| User Story No | Implemented | Evidence or still to implement                                                                                                                                                                                                                                                                                                            |
|---------------|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1             | Yes         |  [sign up evidence](../plot_my_path/static/images/readme-img/Account-onboarding-evidence-1.png),  [sign up fields](../plot_my_path/static/images/readme-img/Account-signup-evidence-2.png),  [account verification email](../plot_my_path/static/images/readme-img/account-verification-email.png)                                        |
| 2             | Yes         | [landing page](../plot_my_path/static/images/readme-img/landing-page-us2.png), [onboarding page1](../plot_my_path/static/images/readme-img/onboarding1-us2.png), [onboarding page 2](../plot_my_path/static/images/readme-img/onboarding2-us2.png), [onboarding page 3](../plot_my_path/static/images/readme-img/onboarding3-us2.png)     |
| 3             | Yes         | [hoempage greeting ](../plot_my_path/static/images/readme-img/homepage-greeting.png), [popular destinations on homepage](../plot_my_path/static/images/readme-img/homepage-popdestinations.png)                                                                                                                                           |
| 4             | Yes         | [profile page](../plot_my_path/static/images/readme-img/profile-page.png)                                                                                                                                                                                                                                                                 |
| 5             | yes         | [all destinations](../plot_my_path/static/images/readme-img/destinations-all.png), [continent filtered results ](../plot_my_path/static/images/readme-img/filtered-destinations.png)                                                                                                                                                      |
| 6             | yes         | [empty search with no results ](../plot_my_path/static/images/readme-img/destination-empty-search.png), [search results after typing](../plot_my_path/static/images/readme-img/destination-search-results.png)                                                                                                                            |
| 7             | yes         | [destination detail page](../plot_my_path/static/images/readme-img/destination-detail.png)                                                                                                                                                                                                                                                |
| 8             | No          | Currently only shows brief description of attraction but backend data is in place for later development.                                                                                                                                                                                                                                  |
| 9             | yes         | [favourite button ](../plot_my_path/static/images/readme-img/favourite-button.png), [saved destination page with no duplicates](../plot_my_path/static/images/readme-img/saved-destinations.png)                                                                                                                                          |
| 10            | yes         | [saved destinations page ](../plot_my_path/static/images/readme-img/saved-destinations.png)                                                                                                                                                                                                                                               |
| 11            | yes         | [wizard form page 1 ](../plot_my_path/static/images/readme-img/wizard-form-1.png), [wizard form page 2](../plot_my_path/static/images/readme-img/wizard-form-2.png), [wizard form page 3 ](../plot_my_path/static/images/readme-img/wizard-form-3.png), [waizard form page 4](../plot_my_path/static/images/readme-img/wizard-form-4.png) |
| 12            | yes         | [if preferences are saved it will match interest in itinerary builder on both drop down and flag up once selected](../plot_my_path/static/images/readme-img/preferences-saved.png)                                                                                                                                                        |
| 13            | yes         | [start date in past error ](../plot_my_path/static/images/readme-img/same-day-error.png), [end date before start date error ](../plot_my_path/static/images/readme-img/past-date-error.png), [no longer than one day error message](../plot_my_path/static/images/readme-img/end-date-error.png)                                          |
| 14            | yes         | [profile redirect with message after free useage](../plot_my_path/static/images/readme-img/profile-page-warning.png)                                                                                                                                                                                                                      |
| 15            | yes         | [trip page](../plot_my_path/static/images/readme-img/trips-page.png)                                                                                                                                                                                                                                                                      |
| 16            | yes         | [deleting a trip warning ](../plot_my_path/static/images/readme-img/trip-deletion-1.png), [deleting a trip confirmation ](../plot_my_path/static/images/readme-img/trip-deletion-2.png)                                                                                                                                                         |
| 17            | yes         | [days display on itinerary page](../plot_my_path/static/images/readme-img/itinerary-page-days.png)                                                                                                                                                                                                                                           |
| 18            | yes         | [adding attraction](../plot_my_path/static/images/readme-img/adding-attraction.png), [no attraction selected error ](../plot_my_path/static/images/readme-img/no-attraction-error.png), [start time error message](../plot_my_path/static/images/readme-img/attraction-start-time-error.png)                                                       |
| 19            | no          | Currently can only remove activity, cannot update it. Feature to be added in later update                                                                                                                                                                                                                                                 |
| 20            | yes         | [normal weather page](../plot_my_path/static/images/readme-img/weather.png), [no weather to display page](../plot_my_path/static/images/readme-img/no-weather.png)                                                                                                                                                                        |
| 21            | yes         | Each trip is assigned to that users id so unless signed in as that user you do not even know if they have any trips planned let alone view them.                                                                                                                                                                                          |
| 22            | yes         | [stripe payment page](../plot_my_path/static/images/readme-img/stripe-payment-page.png), [Cancel and refund button appears so that being charged twice is not an option as you cannot be redirected](../plot_my_path/static/images/readme-img/cancel-refund-button.png)                                                                         |
| 23            | Yes         | [payment success page](../plot_my_path/static/images/readme-img/payment-success.png), [premium memnership badge](../plot_my_path/static/images/readme-img/premium-membership-profile.png)                                                                                                                                                       |
| 24            | Yes         | [payment failed page](../plot_my_path/static/images/readme-img/payment-failed.png)                                                                                                                                                                                                                                                        |
| 25            | Yes         | [cancel button](../plot_my_path/static/images/readme-img/cancel-refund-button.png), [cancel message](../plot_my_path/static/images/readme-img/cancel-message.png), [cancel message 2](../plot_my_path/static/images/readme-img/cancel-message2.png)-                                                                                      |
| 26            | No          | Comes up with matches your criteria but does not give any reasons. Will be added in a later update                                                                                                                                                                                                                                        |
| 27            | Yes         | [contact form](../plot_my_path/static/images/readme-img/contact-form.png), [email confirmation](../plot_my_path/static/images/readme-img/email-confirmation.png)                                                                                                                                                                          |
---
[back to top](#plot-my-path)
### Technologies used
---

| Technology          | Use                                     |
|---------------------|-----------------------------------------|
| Visual Studio Code  | Integrated Development Environment(IDE) |
| React               | Interactive frontend components         |
| DaisyUI             | Component Library                       |
| Tailwind CSS        | CSS Styling                             |
| Django              | Full Stack Framework                    |
| Node.js             | Javascript runtime                      |
| Vite                | frontend react build tool               |
| Python              | Coding language                         |
| Javascript          | Coding language                         |
| HTML                | Webpages                                |
| CSS                 | Styling                                 |
| Neon                | postgresql database                     |
| https://developer.mozilla.org/en-US/observatory/               | Security Testing                        |

[back to top](#plot-my-path)
### Testing
---
#### Lighthouse tests 
---
##### Landing Page
---
**Mobile Tests**

|                   | Performance | Accessibility | Best Practices | SEO |
|-------------------|-------------|---------------|----------------|-----|
| First Test Score  | 78          | 100           | 96             | 91  |
| Second Test Score | 100         | 100           | 96             | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/landing-lighthouse-1.png)
![Lighthouse mobile test 2](../plot_my_path/static/images/readme-img/landing-lighthouse-2.png)

- The first round of mobile testing showed that the Best Practices score was being affected by a console error caused by a missing favicon.ico. I resolved this by creating the favicon, which removed the error.
- I then compressed the landing page image and added meta descriptions to the page. Together, these changes raised the Performance score from 78 to 100 and the SEO score from 91 to 100.
- The Best Practices score remained at 96. The remaining deduction relates to the compressed logo image, which is now displayed at a lower quality than its original. As it is only a logo, the difference is barely noticeable to the average user. Since the compression also improved the Performance score by 22 points, I considered this an acceptable trade-off.

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 91          | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/landing-desktop-lighthouse-1.png)

- Following the mobile testing, all necessary changes had already been applied, so the desktop test achieved 100 in every category except Performance. This was due to layout shifts caused by the page adapting between mobile and desktop views. As the score of 91 was already high, I decided no further changes to the page were necessary.


##### Onboarding Page
---
**Mobile Tests**

|                   | Performance | Accessibility | Best Practices | SEO |
|-------------------|-------------|---------------|----------------|-----|
| First Test Score  | 79          | 96            | 100            | 100 |
| Second Test Score | 93          | 100           | 100            | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/onboarding-lighthouse-1.png)
![Lighthouse mobile test 2](../plot_my_path/static/images/readme-img/onboarding-lighthouse-2.png)

- The first round of mobile testing showed that the MapLibre styles were being loaded on this page even though no map was displayed. All JavaScript runs through main.jsx, which statically imported the itinerary builder, so the builder, MapLibre and its stylesheet were bundled into every page.
- To resolve this, I removed the static import from the top of main.jsx and replaced it with a dynamic import() inside the if (builder) block. The itinerary builder and its map code now only load on pages that use them, which raised the Performance score from 79 to 93.
- To fix the Accessibility score, I changed the div that renders the React onboarding component into a main element. This provided the page with a main landmark, which raised the Accessibility score from 96 to 100.

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 97          | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/onboarding-desktop-lighthouse.png)

- As the mobile fixes had already been applied, the desktop test scored highly in every category. No further changes were needed.

##### Login Page
---
**Mobile Tests**

|                   | Performance | Accessibility | Best Practices | SEO |
|-------------------|-------------|---------------|----------------|-----|
| First Test Score  | 99          | 93            | 100            | 100 |
| Second Test Score | 99          | 93            | 100            | 100 |
| Third Test Score  | 99          | 100           | 100            | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/login-lighthouse-1.png)
![Lighthouse mobile test 2](../plot_my_path/static/images/readme-img/login-lighthouse-2.png)
![Lighthouse mobile test 3](../plot_my_path/static/images/readme-img/login-lighthouse-3.png)

- After the first round of Lighthouse testing, the Accessibility score of 93 was caused by low-contrast text. I resolved this by removing the opacity from the affected text.
- The second test showed two remaining issues: the page had no main landmark for screen readers, and some further text with 70% opacity was failing the contrast ratio check. This text was being styled by allauth UI, so I added a custom CSS rule targeting all form label text to override it.
- I also changed the card containing the allauth forms to a main element, which provided the page with a main landmark. Together, these changes raised the Accessibility score from 93 to 100.

**Having made all nescesary changes on the login page and updating the backgrounds with a new css style all allauth pages are scoring identically to the third mobile test above and ther desktop test below so the results have not been recorded**

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 100         | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/login-desktop-lighthouse.png)

- As the mobile fixes had already been applied, the desktop test scored 100 in every category. No further changes were needed.

##### Home Page
---
**Mobile Tests**

|                   | Performance | Accessibility | Best Practices | SEO |
|-------------------|-------------|---------------|----------------|-----|
| First Test Score  | 77          | 100           | 77             | 100 |
| Second Test Score | 87          | 100           | 77             | 100 |
| Third Test Score  | 93          | 100           | 100            | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/home-lighthouse-1.png)
![Lighthouse mobile test 2](../plot_my_path/static/images/readme-img/home-lighthouse-2.png)
![Lighthouse mobile test 3](../plot_my_path/static/images/readme-img/home-lighthouse-3.png)

- The first round of mobile testing showed that the main issues were image optimisation and a warning on the search bar input.
- To address this, I added a preload for home_img in the head of the page and added a name to the search bar input to remove the warning. This cleared the search bar warning, but on retest the preload did not improve the scores enough and introduced a new warning of its own.
- To fix the image issues, I added the following Cloudinary optimisations to get_image_url
  - c_limit: resizes the image only if it exceeds the specified width, without forcing a crop.
  - w_1080: limits the default image to a maximum width of 1080px.
  - q_auto: automatically adjusts image quality to reduce file size.
  - f_auto: automatically serves an efficient image format supported by the browser.
- I also added get_image_url_srcset, which generates multiple image sizes so the browser can choose the most suitable one for the screen and display size. The same changes were applied to the attractions get_image_url to prevent similar issues from arising there.
- The HTML was then updated to use the new methods, which raised the Performance score from 77 to 93:
- crossorigin anonymous added to img as well to solve cookie issue affecting best practices

img
  src="{{ destination.get_image_url }}"
  srcset="{{ destination.get_image_url_srcset }}"
  alt="{{ destination.name }}"
  crossorigin = "anonymous"
  loading="lazy"
  decoding="async"
  class="w-full h-full object-cover"


**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 100         | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/home-desktop-lighthouse.png)

- As the mobile fixes had already been applied, the desktop test scored highly in every category. No further changes were needed.

##### Upcoming Trips
---
**Mobile Tests**

|                   | Performance | Accessibility | Best Practices | SEO |
|-------------------|-------------|---------------|----------------|-----|
| First Test Score  | 88          | 95            | 100            | 100 |
| Second Test Score | 94          | 100           | 100            | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/my-trips-lighthouse-1.png)
![Lighthouse mobile test 2](../plot_my_path/static/images/readme-img/my-trips-lighthouse-2.png)

- The first round of mobile testing showed that the images were lowering the Performance score because they were being downloaded at the wrong size.
- To resolve this, I added sizes="(max-width: 767px) 100vw, 378px" to the img on the My Trips page, which raised the Performance score from 88 to 94.
- The Accessibility score was being affected by the contrast ratio of the delete button. I changed it from an outline button to a solid error button, which raised the Accessibility score from 95 to 100.
- The favicon also appeared blurry on larger screens, so I replaced it with a larger image, which resolved the issue.

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 100         | 100           | 100            | 100 |

- As the mobile fixes had already been applied, no further changes were needed for the desktop view.

##### Destinations
---
**Mobile Tests**

|                   | Performance | Accessibility | Best Practices | SEO |
|-------------------|-------------|---------------|----------------|-----|
| First Test Score  | 93          | 100           | 100            | 100 |
| Second Test Score | 97          | 100           | 100            | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/destinations-lighthouse-1.png)
![Lighthouse mobile test 2](../plot_my_path/static/images/readme-img/destinations-lighthouse-2.png)

- Although the scores were already high, the first round of mobile testing showed the same image sizing issue that had occurred throughout testing.
- To resolve this, I added the same sizes attribute used on the My Trips page to the img, which raised the Performance score from 93 to 97.

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 100         | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/destinations-desktop-lighthouse.png)

- As the mobile fixes had already been applied, no further changes were needed for the desktop view.

##### Destination Detail
---
**Mobile Tests**

|                   | Performance | Accessibility | Best Practices | SEO |
|-------------------|-------------|---------------|----------------|-----|
| First Test Score  | 97          | 92            | 100            | 100 |
| Second Test Score | 96          | 100           | 100            | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/destination-detail-lighthouse-1.png)
![Lighthouse mobile test 2](../plot_my_path/static/images/readme-img/destination-detail-lighthouse-2.png)

- The first round of mobile testing showed that the ARIA attributes on the favourite button were failing the Accessibility audit.
- The aria-pressed value was being rendered with extra whitespace and line breaks, so it was not a valid true or false value. I moved the template logic onto a single line so the attribute renders exactly as true or false, which raised the Accessibility score from 92 to 100.
- All other scores were already high, so no further changes were needed.

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 99          | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/destination-detail-desktop-lighthouse.png)

- As the mobile fixes had already been applied, the desktop test passed first time and no further changes were needed.


##### Trip Builder(originally trips.html)

---
**Mobile Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 99          | 100           | 100            | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/trip_builder-lighthouse-1.png)

- As all of my pages inherit from base.html, the changes made while testing earlier pages were applied sitewide where possible. This is reflected in the scores, which were high on the first test for this page.
- I also renamed the file to trip_builder and updated all links to the old filename, so that the name describes what the page does before anyone looks at the code.

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 100         | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/trip_builder-desktop-lighthouse.png)

- As with the mobile tests, no further changes were required after testing.

##### Itinerary Builder
---
**Mobile Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 84          | 100           | 100            | 100 |

![Lighthouse mobile test](../plot_my_path/static/images/readme-img/itinerary_builder-lighthouse-1.png)

- The first round of mobile testing showed that the main factor affecting Performance was document request latency.
- The site is hosted on Render's free tier, where server response time is outside of my control, so this was recorded as a known hosting limitation.
- The page also has a lot to load. It hosts a React component that brings in three separate components, along with an interactive map and weather data.
- With all of this in mind, the score of 84 was considered good for the amount happening on the page, and no further changes were made.

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 99          | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/itinerary-builder-desktop-lighthouse.png)

- The desktop test scored 99, which supports the point that the mobile score was held back by document request latency and the throttled mobile conditions rather than the page itself. No further action was needed on this page.

##### Profile Page
---
**Mobile Tests**

|                   | Performance | Accessibility | Best Practices | SEO |
|-------------------|-------------|---------------|----------------|-----|
| First Test Score  | 99          | 95            | 100            | 100 |
| Second Test Score | 99          | 100           | 100            | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/profile-lighthouse-1.png)
![Lighthouse mobile test 2](../plot_my_path/static/images/readme-img/profile-lighthouse-2.png)

- The first round of mobile testing flagged the same contrast ratio problem on the cancel button that had appeared on a previous page.
- To resolve this, I changed the button from btn-error btn-outline to a solid btn-error, which raised the Accessibility score from 95 to 100.
- All other scores were already high, so no further changes were needed.

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 100         | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/profile-desktop-lighthouse.png)

- As the mobile fixes had already been applied, no further changes were needed for the desktop view.

##### Saved Destinations(previously favourite_destinations)
---
**Mobile Tests**

|                   | Performance | Accessibility | Best Practices | SEO |
|-------------------|-------------|---------------|----------------|-----|
| First Test Score  | 84          | 98            | 77             | 100 |
| Second Test Score | 78          | 98            | 100            | 100 |
| Third Test Score  | 98          | 100           | 100            | 100 |

![Lighthouse mobile test 1](../plot_my_path/static/images/readme-img/saved-destination-lighthouse-1.png)
![Lighthouse mobile test 2](../plot_my_path/static/images/readme-img/saved-destination-lighthouse-2.png)
![Lighthouse mobile test 3](../plot_my_path/static/images/readme-img/saved-destination-lighthouse-3.png)

- The first round of mobile testing showed that when I updated get_image_url and get_image_url_srcset, I had not updated the images on this page. This caused both the Performance and Best Practices scores to drop, due to oversized images and third-party cookies.
- I then updated the img and added the srcset, but did not update the sizes attribute, so the Performance score dropped to 78. The Best Practices score rose to 100 at this point, as the third-party cookie issue was resolved.
- I also discovered that I had previously deleted an h2 without updating the h3, so the page had an h1 followed by an h3. This skipped heading level was affecting the Accessibility score.
- I updated the sizes attribute and changed the h3 to an h2. The final test scored 98 for Performance and 100 for Accessibility, which I considered acceptable.

**Desktop Tests**

|                  | Performance | Accessibility | Best Practices | SEO |
|------------------|-------------|---------------|----------------|-----|
| First Test Score | 100         | 100           | 100            | 100 |

![Lighthouse desktop test](../plot_my_path/static/images/readme-img/saved-destination-desktop-lighthouse.png)

- As the mobile fixes had already been applied, no further changes were needed for the desktop view.

[back to top](#plot-my-path)
#### HTML tests 
---
[back to top](#plot-my-path)
#### CSS tests 
---
[back to top](#plot-my-path)
#### Python code validation
---

All code has been formatted to PEP8 style standards using black and the command 
black . and then checked to confirm as is shown below

black --check .
All done! ✨ 🍰 ✨
54 files would be left unchanged.
(.venv) 

[back to top](#plot-my-path)

#### JSX Testing
---

- Testing was carried out use vitest using the following command 
npx vitest run assets/js/tests/filename.test.js

##### Utils.js testing 
**The Tests**
---

The utility function tests verify the behaviour of the application's reusable helper functions.

**getCookie()**
- Checks that the function correctly retrieves the value of an existing cookie.
- Confirms that null is returned when the requested cookie does not exist.
- Tests that equals signs within cookie values are preserved.
- Verifies that URL-encoded cookie values are correctly decoded.

**formatActivityTime()**
- Checks that empty or null values return the default time of 00:00.
- Verifies that ISO datetime strings are correctly converted into HH:MM format.
- Checks that existing time strings are correctly shortened to HH:MM.
- Handles ISO datetime strings that contain no time component.

These tests help ensure that cookie handling and activity time formatting work reliably throughout the application.

**The Results**
---
npx vitest run assets/js/tests/utils.test.js

 RUN  v5.1.1 C:/Users/devil/Documents/milestone-four/plot_my_path

 ✓ assets/js/tests/utils.test.js (9 tests) 15ms  
   ✓ getCookie (4)  
     ✓ returns the value of an existing cookie 11ms  
     ✓ returns null when the cookie does not exist 1ms  
     ✓ preserves equals signs in cookie values 0ms  
     ✓ decodes URL-encoded cookie values 0ms  
   ✓ formatActivityTime (5)  
     ✓ returns 00:00 when given an empty value 0ms  
     ✓ returns 00:00 when given null 0ms  
     ✓ extracts the time from an ISO datetime string 0ms  
     ✓ returns an existing time in HH:MM format 0ms  
     ✓ returns 00:00 when an ISO datetime has no time after T 0ms  

 Test Files  1 passed (1)  
      Tests  9 passed (9)  

##### ActivityList.jsx Testing
---
**The Tests**

The ActivityList component tests verify that itinerary activities are displayed correctly and that users can interact with them.

The tests cover:

- Displaying activity names by matching activities to their corresponding attractions using attraction IDs.
- Formatting and displaying activity start and end times.
- Displaying attraction entry costs.
- Showing an indicator when an attraction matches the user's interests.
- Providing a fallback message when an attraction cannot be found.
- Calling the removal callback with the correct activity ID when the user clicks the Remove button.
- Disabling removal buttons and displaying a loading state while an activity is being deleted.
- Displaying error messages when an error is provided.
- Showing an appropriate empty-state message when no activities exist.

These tests help ensure that itinerary information is presented accurately and that the activity removal interface behaves as expected.

**The Results**
---
npx vitest run assets/js/tests/ActivityList.test.jsx

 RUN  v5.1.1 C:/Users/devil/Documents/milestone-four/plot_my_path

 ✓ assets/js/tests/ActivityList.test.jsx (9 tests) 265ms  
   ✓ ActivityList (9)  
     ✓ displays the activities and their attraction names 45ms  
     ✓ displays activity start and end times 8ms  
     ✓ displays the attraction entry costs 7ms  
     ✓ displays a preference match indicator when applicable 4ms  
     ✓ displays a fallback when an attraction cannot be found 3ms  
     ✓ calls onRemove with the activity ID when Remove is clicked 175ms  
     ✓ disables all Remove buttons while an activity is being deleted 11ms  
     ✓ displays an error message when an error is provided 7ms  
     ✓ displays an empty message when there are no activities 2ms  

 Test Files  1 passed (1)  
      Tests  9 passed (9)

##### AddActivityForm.jsx-Testing
--- 
**The Tests**

The AddActivityForm component tests verify that users can select attractions, enter activity times and add activities to their itinerary.

The tests cover:

- Rendering the attraction selector and start and end time inputs.
- Displaying the available attractions.
- Validating that an attraction has been selected.
- Validating that the start time is earlier than the end time.
- Filtering attractions when the user selects the "For you" option.
- Successfully submitting a new activity and calling the `onAdded` callback.
- Verifying that the API request contains the correct URL, HTTP method, headers, CSRF token and activity data.
- Displaying an error when the API request fails.

These tests help ensure that the activity form validates user input correctly and communicates reliably with the Django backend.

**The Results**
---

npx vitest run assets/js/tests/AddActivityForm.test.jsx

 RUN  v5.1.1 C:/Users/devil/Documents/milestone-four/plot_my_path

 ✓ assets/js/tests/AddActivityForm.test.jsx (8 tests) 1111ms
   ✓ AddActivityForm (8)
     ✓ renders the attraction selector and time inputs 162ms
     ✓ displays the available attractions 19ms
     ✓ displays a validation error when no attraction is selected 51ms
     ✓ displays a validation error when the start time is after the end time 430ms
     ✓ filters attractions when the For you checkbox is selected 124ms
     ✓ submits the selected activity successfully 107ms
     ✓ sends the correct request details when adding an activity 111ms
     ✓ displays an error when the API request fails 104ms

 Test Files  1 passed (1)
      Tests  8 passed (8)

##### itinerary_builder.jsx Testing 
**The Tests** 
---
The ItineraryBuilder component tests verify that users can manage their daily itinerary, navigate between trip days and monitor their remaining budget.

The tests cover:
- Displaying itinerary days in the correct order.
- Showing a message when no itinerary days are available.
- Navigating forwards and backwards between itinerary days.
- Disabling navigation buttons when the first or last day is selected.
- Calculating the daily budget and remaining budget based on planned activities.
- Adding activities to the selected itinerary day.
- Successfully deleting activities through the Django backend.
- Displaying an error when an activity cannot be deleted.
- Rendering the map and weather components.

Child components are mocked to allow the tests to focus on the functionality and state management of ItineraryBuilder independently.

These tests help ensure that itinerary management, day navigation, budget calculations and communication with the backend work correctly.

**The Results**
---
npx vitest run assets/js/tests/ItineraryBuilder.test.jsx

 RUN  v5.1.1 C:/Users/devil/Documents/milestone-four/plot_my_path

 ✓ assets/js/tests/ItineraryBuilder.test.jsx (8 tests) 455ms
 
   ✓ ItineraryBuilder (8)
     ✓ renders the first itinerary day in day-number order 178ms
     ✓ displays a message when no itinerary days are available 4ms
     ✓ allows the user to move between itinerary days 118ms
     ✓ calculates the daily budget and remaining budget 7ms
     ✓ adds a new activity to the selected day 44ms
     ✓ deletes an activity successfully 37ms
     ✓ displays an error when deleting an activity fails 59ms
     ✓ renders the map and weather components 5ms

 Test Files  1 passed (1)
      Tests  8 passed (8)

##### ItineraryMap.jsx testing 
---
**The Tests**
---

The ItineraryMap component tests verify that the interactive map correctly displays available attractions and scheduled itinerary stops using MapLibre.

The tests cover:
- Initialising the map with the supplied destination coordinates.
- Using fallback coordinates when the destination coordinates are invalid.
- Creating separate GeoJSON sources and layers for available attractions and planned stops.
- Excluding scheduled attractions from the available attractions source.
- Adjusting the map view to fit multiple scheduled stops.
- Centring the map on a single scheduled stop.
- Updating map sources when itinerary stops or attractions change.
- Opening popups when map features are clicked.
- Cleaning up the map and resize observer when the component unmounts.

MapLibre is mocked to allow the component's map interactions, data updates and lifecycle behaviour to be tested without loading an actual map.

These tests help ensure that map data remains synchronised with the itinerary and that map resources are properly managed.

**The Results**
---
 npx vitest run assets/js/tests/ItineraryMap.test.jsx

 RUN  v5.1.1 C:/Users/devil/Documents/milestone-four/plot_my_path

 ✓ assets/js/tests/ItineraryMap.test.jsx (9 tests) 94ms
   ✓ ItineraryMap (9)
     ✓ initialises the map using the supplied destination coordinates 59ms
     ✓ uses the fallback centre when destination coordinates are invalid 5ms
     ✓ creates the attraction and planned-stop sources and layers when the map loads 6ms
     ✓ excludes scheduled attractions from the available attractions source 4ms
     ✓ fits the map around multiple scheduled stops 3ms
     ✓ centres the map on a single scheduled stop 3ms
     ✓ updates map sources when the attractions or stops change 5ms
     ✓ opens a popup when a map feature is clicked 3ms
     ✓ disconnects the resize observer and removes the map on unmount 3ms

 Test Files  1 passed (1)
      Tests  9 passed (9)

##### WeatherPanel.jsx Testing
--- 
**The tests**
---

The WeatherPanel component tests verify that the correct weather forecast is displayed for the currently selected itinerary day.

The tests cover:
- Displaying the destination name, itinerary day number and date.
- Showing the weather conditions for the selected day.
- Displaying the maximum and minimum temperatures.
- Displaying the probability of rain.
- Ensuring weather information from other dates is not displayed.
- Displaying an error message when weather data cannot be loaded.
- Showing a fallback message when no weather data is available.
- Handling weather data that does not contain a forecast for the selected date.

These tests help ensure that users see accurate weather information for the day they are planning.

**The Results**
---
 npx vitest run assets/js/tests/WeatherPanel.test.jsx

 RUN  v5.1.1 C:/Users/devil/Documents/milestone-four/plot_my_path

 ✓ assets/js/tests/WeatherPanel.test.jsx (6 tests) 176ms
   ✓ WeatherPanel (6)
     ✓ displays the destination and selected itinerary day 140ms
     ✓ displays the forecast matching the selected day 11ms
     ✓ does not display weather for a different day 4ms
     ✓ displays an error message when an error is provided 8ms
     ✓ displays a message when no weather data is available 6ms
     ✓ displays a message when weather data does not match the selected day 4ms

 Test Files  1 passed (1)
      Tests  6 passed (6)

##### SearchBar.jsx Testing
--- 
**The tests**
---

#### Search Bar Tests (`SearchBar.test.jsx`)

The SearchBar component tests verify that users can search for destinations and view matching results returned by the Django API.

The tests cover:
- Rendering the destination search input.
- Debouncing search requests by 300 milliseconds.
- Sending API requests after the debounce period.
- Encoding special characters in search queries.
- Resetting the debounce timer when the search query changes.
- Displaying a loading indicator while requests are pending.
- Displaying destination search results, including names and countries.
- Generating destination links using a supplied base URL.
- Using a default destination URL when no base URL is provided.
- Displaying destination images with appropriate alternative text.
- Clearing search results when the search input is emptied.

The Fetch API is mocked to test the component without making actual requests to the Django backend.

These tests help ensure that destination searches are responsive, efficient and display the correct results.

**The Results**
---
npx vitest run assets/js/tests/SearchBar.test.jsx

 RUN  v5.1.1 C:/Users/devil/Documents/milestone-four/plot_my_path

 ✓ assets/js/tests/SearchBar.test.jsx (11 tests) 246ms
   ✓ SearchBar (11)
     ✓ renders the destination search input 43ms
     ✓ does not search before the 300ms debounce period 10ms
     ✓ searches after the 300ms debounce period 7ms
     ✓ encodes special characters in the search query 5ms
     ✓ resets the debounce timer when the query changes 5ms
     ✓ displays the loading indicator while the search request is pending 14ms
     ✓ displays destination results returned by the API 12ms
     ✓ uses the supplied base URL when creating destination links 112ms
     ✓ uses the default destination URL when no base URL is supplied 13ms
     ✓ displays the destination image and its alternative text 13ms
     ✓ clears the results when the search query is emptied 9ms

 Test Files  1 passed (1)
      Tests  11 passed (11)

##### Onboarding.jsx testing
---
** The Tests**
---

#### Onboarding Tests (`Onboarding.test.jsx`)

The Onboarding component tests verify that new users are presented with an introductory carousel explaining the main features of the application.

The tests cover:
- Displaying the main onboarding heading.
- Rendering all three introductory sections.
- Displaying the correct descriptions for each section.
- Providing a skip link to the home page.
- Providing next and previous navigation links between carousel slides.
- Providing a Get Started link on the final slide.
- Displaying all three onboarding images with descriptive alternative text.
- Using the Django static URL when loading onboarding images.
- Falling back to the default static directory when the Django static URL is unavailable.

These tests help ensure that users can navigate the onboarding experience and understand the main features of the application.

**The Results**
---
npx vitest run assets/js/tests/Onboarding.test.jsx

 RUN  v5.1.1 C:/Users/devil/Documents/milestone-four/plot_my_path

 ✓ assets/js/tests/Onboarding.test.jsx (9 tests) 294ms
   ✓ Onboarding (9)
     ✓ displays the main onboarding heading 160ms
     ✓ displays all three onboarding sections 19ms
     ✓ displays the introductory descriptions 9ms
     ✓ provides a skip link to the home page 18ms
     ✓ provides next and previous links between slides 22ms
     ✓ provides a Get Started link to the home page 14ms
     ✓ displays all three onboarding images with descriptive alternative text 18ms
     ✓ uses the Django static URL for onboarding images 17ms
     ✓ uses the default static URL when Django static URL is unavailable 13ms

 Test Files  1 passed (1)
      Tests  9 passed (9)

##### main.jsx Testing 
--- 
**The Tests**

#### Main JavaScript Tests (`main.test.jsx`)

The main JavaScript tests verify the functionality that connects the Django templates with the React components and handles interactive elements across the application.

The tests cover:
- Mounting the Onboarding, SearchBar and ItineraryBuilder React components into their correct Django template elements.
- Initialising the theme toggle using the current HTML theme.
- Switching between the fantasy and sunset themes.
- Saving the selected theme to localStorage.
- Sending POST requests when users add or remove destinations from their favourites.
- Updating favourite button icons, colours and accessibility labels.
- Preventing requests when a favourite button is already disabled.
- Handling errors when favourite requests fail.
- Sending checkout requests with the correct URL, HTTP method and CSRF token.
- Displaying appropriate error messages when checkout cannot proceed or payment processing fails.
- Adding a fade-out class to Django alert messages after three seconds.

The tests mock React mounting and API requests so that the application's JavaScript functionality can be tested independently of the Django backend.

**The Results**
--- 

 npx vitest run assets/js/tests/main.test.jsx

 RUN  v5.1.1 C:/Users/devil/Documents/milestone-four/plot_my_path

 ✓ assets/js/tests/main.test.jsx (15 tests) 265ms
   ✓ main.jsx (15)
     ✓ mounts React components into the correct Django template elements 19ms
     ✓ initialises the theme checkbox using the current HTML theme 1ms
     ✓ changes the theme to fantasy when the toggle is unchecked 2ms
     ✓ changes the theme to sunset when the toggle is checked 1ms
     ✓ does not throw an error when the theme toggle is missing 1ms
     ✓ sends a POST request when a favourite button is clicked 16ms
     ✓ updates the favourite button when an attraction is added to favourites 7ms
     ✓ updates the favourite button when an attraction is removed from favourites 16ms
     ✓ does not send a request when a favourite button is disabled 2ms
     ✓ logs an error when the favourite request fails 17ms
     ✓ sends a POST request when the checkout button is clicked 15ms
     ✓ displays an error when checkout cannot proceed 16ms
     ✓ displays a fallback message when checkout returns no error 17ms
     ✓ displays an error when payment processing fails 15ms
     ✓ adds the fade-out class to alerts after three seconds 7ms

 Test Files  1 passed (1)
      Tests  15 passed (15)
[back to top](#plot-my-path)

#### API Testing 
---
[back to top](#plot-my-path)

#### Security 
---
Content Security Policy
---

To make my project as secure as possible, I decided to add a Content Security Policy (CSP). An enforced CSP reduces the risk of Cross-Site Scripting (XSS), clickjacking and the unauthorised loading of external resources. I initially set the policy up in report-only mode so I could test it and identify any violations without breaking the site. Once I had reviewed the reports, I switched to enforcement using Django's SECURE_CSP setting. The following changes were needed to make it work effectively:

- **Removed inline styles:** The landing page background image was triggering CSP violations because it was set using an inline HTML style attribute. I moved it into a class in my CSS stylesheet instead. This removed the need to permit inline styles in my CSP, and the image still loads as before.
- **Updated the policy for Google OAuth sign-in:** When I first enforced the CSP, Google sign-in stopped working. After investigating, I discovered that the OAuth flow redirects to Google's authentication endpoint, which the CSP was blocking. Adding form-action with Google's domain fixed this, and on retesting the sign-in worked perfectly.

The CSP configuration is as follows:

| Directive                                         | Purpose                                                                                                               |
|---------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------|
| `default-src 'self'`                              | Restricts resources to the application's own origin by default.                                                       |
| `script-src 'self' 'nonce-...'`                   | Allows scripts from the application's own origin, plus explicitly authorised inline scripts using a per-response nonce. |
| `img-src 'self' data: https://res.cloudinary.com` | Allows local images, data URI images and images hosted by Cloudinary.                                                 |
| `base-uri 'self'`                                 | Prevents unauthorised external base URLs from being used.                                                             |
| `form-action 'self' https://accounts.google.com`  | Restricts form submissions to the application and permits the Google OAuth authentication flow.                       |
| `frame-ancestors 'none'`                          | Prevents the application from being embedded in frames, protecting against clickjacking.                              |
| `object-src 'none'`                               | Blocks potentially unsafe embedded objects such as Flash.                                                             |
| `connect-src 'self' https://tiles.openfreemap.org` | Restricts network connections to the application and the OpenFreeMap tile service.                                   |

![security test 1](../plot_my_path/static/images/readme-img/security-test-1.png)
 
 Having already carried out quite an extensive CSP policy the only error that flagged up following the first security test was the Strict Transport Security (HSTS) which had been set to one hour previously. THe recommended was one year which has since been adjusted and the second test below confirms that all tests passed. 

 ![security test 2](../plot_my_path/static/images/readme-img/security-test-2.png)

Results 

#### Automated Testing
---

#### Django Testing – Using Django's Testing Suite

---
- All django testing was carried out using the command python manage.py test "appname" --keepdb
- All sections have their corrosponding commit number for when they were originaly carried out underneath each section header 
##### Core Testing – The Tests

- Core tests ran at commit **173448e**.

**Pages**

- The landing page and onboarding page load for anyone and use their expected templates.
- The homepage requires login: a logged-out visitor is redirected to the login page.
- The homepage greeting depends on the time of day: "Good morning" at 9am, "Good afternoon" at 2pm and "Good evening" at 8pm. The clock is mocked, so the tests give the same result whenever they run.

**Contact page**

- The page loads and uses the correct contact template.
- For a logged-in user, the form is pre-filled with their first name and email address.
- A valid submission sends one email containing the message and redirects back to the contact page. Django's in-memory test mailbox is used.
- An invalid submission re-renders the form and sends no email.

**Signup form**

- The form is valid with a first and last name, and invalid when either is missing.
- Calling signup saves the first and last name onto the user.

**Contact form**

- The form is valid with a name, email, subject and message.
- The form is invalid when any required field is missing.
- A malformed email address is rejected.

##### Core Testing – Results

System check identified no issues (0 silenced).
.........................................
----------------------------------------------------------------------
Ran 41 tests in 33.193s

OK
Preserving test database for alias 'default'...

---

##### Accounts Model Testing – The Tests

- Accounts model tests ran at commit **df124fc**.

**Travel Preference**

- A new preference defaults every interest flag (e.g. walking and culture) to False, and its string representation is "Preferences for <username>".
- A travel style outside the allowed choices is rejected by validation.
- Deleting a user deletes their travel preferences.

**Saved Destination**

- Its string representation reads "<username> saved <destination>", and a creation timestamp is set automatically.
- A user cannot save the same destination twice.
- Different users can save the same destination.
- Deleting a destination removes saved records pointing to it.
- Deleting a user removes all their saved destination records.


##### Accounts View Testing – The Tests
- Account view tests carried out at **commit 7e57d3c**

Accounts view tests cover authentication, profile information, saved destinations and favourite functionality.

All views are tested to confirm they require login and redirect logged-out users to the login page.

**Profile page**

- A signed-in user receives the correct profile template and sees their username.

**Favourite destinations**

- A user sees only their own saved destinations and cannot see another user's saved destinations.

**Toggle favourite**

- The first POST request saves the destination and returns is_favourite": true.
- A second POST request removes the saved destination and returns is_favourite": false.
- GET requests are rejected.
- An unknown destination returns a 404 response.
- Toggling one user's favourite does not affect another user's saved destinations.

##### Accounts Testing – Results

System check identified no issues (0 silenced).
................
----------------------------------------------------------------------
Ran 16 tests in 16.829s

OK
Preserving test database for alias 'default'...

---

##### Destinations Model Testing – The Tests

- Destinations model tests ran at commit **72fe012**.
**destinations model retested following updates to cloudinary get_image_url** 

**Country**

- Its string representation is the country name.
- The natural key is the name, and looking a country up by natural key returns the correct record.
- Looking up an unknown country by natural key raises DoesNotExist.

**Destination**

- Its string representation is the destination name.
- The natural key is the slug, and lookup by natural key works.
- Slugs must be unique, enforced by a database constraint.
- The get_image_url property builds the image URL from the Cloudinary cloud name and the destination slug, with image optimisation transformations (c_limit, w_1080, q_auto, f_auto) to reduce file size and serve suitable image formats. It only builds a string, so no request is made to Cloudinary.
- The get_image_url_srcset property generates multiple optimised image URLs at widths of 384, 576, 768 and 1080 pixels. It uses the same q_auto and f_auto transformations, with the width varying for each entry, so the browser can select an appropriate image size.
- Destinations are accessible through their country, and deleting a country deletes its destinations.

**Attraction**

- Its string representation is the attraction name, and the rating is optional.
- The same slug cannot be used twice within one destination, but can be reused in a different destination.
- The get_image_url property builds the image URL from the Cloudinary cloud name and the attraction slug, using the same optimisation transformations (c_limit, w_1080, q_auto, f_auto). It only builds a string, so no request is made to Cloudinary.
- The get_image_url_srcset property generates multiple optimised image URLs at widths of 384, 576, 768 and 1080 pixels. It uses the same q_auto and f_auto transformations, with the width varying for each entry, so the browser can select an appropriate image size.
- Attractions are accessible through their destination, and deleting a destination deletes its attractions.

##### Destinations View Testing – The Tests

- Destination view tests ran at commit **3482b9a15**.

All four views require login: logged-out visitors are redirected to the login page.

**Destination list**

- By default, every destination is shown and the selected continent is "all".
- Filtering by continent returns only matching destinations.
- Continent filtering ignores letter case.
- An unknown continent returns an empty list rather than an error.
- The continent dropdown values are distinct and sorted alphabetically.

**Destination detail**

- The correct destination and template are used, and an unknown destination ID returns a 404.
- Only that destination's attractions are listed.
- The "is favourite" flag is false by default.
- The flag becomes true once the current user has saved the destination.
- Another user's saved destination does not affect the current user's favourite status.

**Search (JSON)**

- A missing or blank query returns an empty result list.
- Matching is partial and case-insensitive.
- A query with no matches returns an empty list.
- Each result contains the destination ID, name, slug, description, cost (as a string) and image URL.
- Results are capped at 10.

**Popular destinations (JSON)**

- Returns an empty list when there are no destinations.
- Returns all destinations when there are fewer than three.
- Returns at most three destinations when more are available.
- The selection is random, so the tests check the number of results rather than which destinations are returned.
- This view does not currently have a URL, so the tests call it directly using Django's RequestFactory.

##### Destinations Testing – Results

System check identified no issues (0 silenced).  
..........................................
----------------------------------------------------------------------
Ran 42 tests in 15.698s

OK
Preserving test database for alias 'default'...

##### Destinations Retest-result

System check identified no issues (0 silenced).
............................................
----------------------------------------------------------------------
Ran 44 tests in 15.627s

OK
Preserving test database for alias 'default'...
---

##### Payments Model Testing – The Tests
**Retesting done after cloudinary image fetching was updated for better lighthouse scores.**
- Payments model tests ran at commit **72fe012**.

**Payment model**

- Its string representation contains the username, amount and currency.
- A new payment defaults to GBP and a pending status.
- amount_pounds converts the stored pence amount into pounds (1999 becomes 19.99).
- The created_at timestamp is set automatically.
- The Stripe payment ID must be unique, enforced by a database constraint.
- A negative payment amount fails validation.
- Payments are accessible through their associated user.

**PremiumMembership model**

- Its string representation contains the username and membership status.
- A new membership defaults to inactive.
- is_active returns true for an active membership and false for an inactive one.
- The created_at timestamp is set automatically.
- A membership is accessible through both its associated user and payment.

##### Payment Views Testing – The Tests

- Payment view testing carried out from **commit 2a9e879 to commit 9708d8c**

**Checkout**

- The checkout page loads for a logged-in user.
- Logged-out users are redirected away from checkout.
- Users who already have an active membership are redirected away from checkout.
- Creating a checkout session returns the Stripe checkout URL as JSON.
- Users who already have an active membership cannot create a new checkout session (409 response), and Stripe is not called.
- The create checkout session view only accepts POST requests.

**Payment success**

- A request with no session ID returns an error (400).
- A paid session creates a payment record and an active membership.
- A session belonging to a different user is rejected (403), and nothing is saved.
- An unpaid session is rejected (400), and nothing is saved.
- Loading the success page twice for the same session does not create duplicate payments or memberships.

**Payment failed**

- The payment failed page loads successfully.
- An error message passed in the URL is displayed on the page.

**Stripe webhook**

- A paid checkout.session.completed event creates a payment and an active membership.
- An unpaid checkout.session.completed event is accepted but creates no payment.
- An invalid payload or signature returns an error (400).
- A charge.refunded event marks the payment as refunded and sets the membership to inactive.
- The webhook only accepts POST requests.

**Refunds**

- A refund is allowed within 14 days of the membership start date.
- A refund is not allowed if the membership has no start date or started more than 14 days ago.
- The refund view only accepts POST requests.
- Logged-out users are redirected away from the refund view.
- A successful refund calls Stripe once, marks the payment as refunded and sets the membership to inactive.
- No refund is processed for a membership older than 14 days or for a membership that is not active. In both cases, the user is redirected.

##### Payments Testing – Results

Found 39 test(s).
Using existing test database for alias 'default'...
System check identified no issues (0 silenced).
.......................................
----------------------------------------------------------------------
Ran 39 tests in 66.204s

OK
Preserving test database for alias 'default'...

---

##### Trips Model Testing – The Tests

---

Trips model testing covers the Trip, TripDay, PlannedActivity and Recommendation models.

**Trip, TripDay and PlannedActivity models**

- The string form of a trip is its name, a day is "Day N - trip name", and an activity is the attraction name followed by its start time.
- A new activity defaults to a scheduled status.
- The trip's absolute URL returns the correct itinerary builder URL.
- A budget that is too large fails validation.
- Deleting a user deletes their trips.
- Deleting a trip deletes its days and planned activities.

**Recommendation model**

- A recommendation can be created with the correct score, reason, user, trip and attraction.
- The string representation includes the username, attraction name and recommendation score.
- Recommendations are ordered by score, with the highest-scoring recommendation first.
- Deleting a user deletes their recommendations.
- Deleting a trip deletes its recommendations.
- Deleting an attraction deletes its recommendations.

##### Trips View Testing – The Tests

-- All trip views and forms testing carried out from **commit efca79f to commit 994e04**
 

**My trips**

- Logged-out users are redirected to the login page.
- Users only see their own trips, never another user's.

**Delete trip**

- A POST request deletes the trip and redirects to the my trips page.
- A user cannot delete another user's trip (404), and the trip is kept.

**Itinerary builder**

- Logged-out users are redirected to the login page.
- Another user's trip returns a 404.
- The page renders the correct template and passes the trip in the context.
- A day is generated for every date of the trip (a five-day trip gives five days) and saved to the database.

**Weather**

- The weather API response is mapped to the fields the site uses (date, maximum and minimum temperature, conditions, chance of rain and icon), and any unrelated fields are dropped.
- The API call is mocked to prevent an actual external request.

**Add activity**

- Logged-out users are redirected to the login page and nothing is saved.
- Another user's trip returns a 404 and nothing is saved.
- Each required field (attraction, start time and end time) is checked in turn, and leaving any one out returns an error (400).
- A valid request creates the activity (201), returns its details as JSON and saves it with the correct order and a scheduled status.
- The response includes the attraction ID, start and end times, order, status and notes.

**Delete activity**

- Deleting an activity removes it from the database and returns a success response (200) with a confirmation message.
- Another user's activity returns a 404 and the activity is kept.

**Wizard forms**

- The preferences form is valid with just a travel style, and optional preference checkboxes default to false.
- Travel style is required.
- The destination form is valid with a destination and trip name, and both fields are required.
- The trip details form accepts a future start date, end date and budget.
- A start date in the past is rejected with an error message.
- The review form is valid when empty.

##### Trips Permissions Testing – The Tests
- Permission tests carried out at **commit 94e3ae2
as well as some missing view tests** 
**Premium membership**

- A user without a membership is not considered premium.
- A user with an active premium membership is recognised as a premium user.

**Trip creation limits**

- A free user can create only one trip. Once a trip exists, they cannot create another.
- A premium user can create multiple trips.

##### Trip Creation Wizard Testing – The Tests

**Create trip**

- Logged-out users are redirected to the login page.
- A free user who already has a trip is redirected to their profile with a message explaining the free trip limit.
- The wizard steps advance in order: preferences, destination, details, then review.
- Completing the wizard creates the trip with the correct name, destination and budget, saves the user's travel preferences, and redirects to the itinerary builder for the new trip.

##### Trips Testing – Results

System check identified no issues (0 silenced).
.........................................
----------------------------------------------------------------------
Ran 41 tests in 33.193s

OK
Preserving test database for alias 'default'...

---

[back to top](#plot-my-path)

#### Contrast tests 
---
| Theme   | Primary colour          | background colour     | Contrast Result | Evidence                                                                           |
|---------|-------------------------|-----------------------|-----------------|------------------------------------------------------------------------------------|
| Sunset  | primary(#FF865B)        | bg-base-100(#121C22)  | Pass            | [sunset-base-100](./static/images/readme-img/text-colour-bg-base-100-sunset.png)   |
| Sunset  | primary(#FF865B)        | bg-baser-200(#0E171E) | Pass            | [sunset-base-200](./static/images/readme-img/text-colour-bg-base-200-sunset.png)   |
| Fantasy | custom primary(#322EB5) | bg-base-100(#ffffff)  | Pass            | [fantasy-base-100](./static/images/readme-img/text-colour-bg-base-100-fantasy.png) |
| Fantasy | custom-primary(#322EB5) | bg-base-200(#E8E8E8)  | Pass            | [fantasy-base-200](./static/images/readme-img/text-colour-bg-base-200-fantasy.png) |
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

##### Running the project locally

##### Prerequisites
| Prerequisities             	|                                                                                                                                                                                                                                                                                                                                                                                                                                                           	|
|----------------------------	|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| Python 3.13+               	|                                                                                                                                                                                                                                                                                                                                                                                                                                                           	|
| Node.js and npm            	|                                                                                                                                                                                                                                                                                                                                                                                                                                                           	|
| Accounts and API keys for: 	| [Google Oauth](https://console.cloud.google.com/)                                                                                                                                                                                                                                                                                                                                                                                                         	|
|                            	| [Cloudinary](https://cloudinary.com/)                                                                                                                                                                                                                                                                                                                                                                                                                     	|
|                            	| [Visual Crossing-weather](https://www.visualcrossing.com/weather-api/?gad_source=1&gad_campaignid=24350121815&gbraid=0AAAAAD5PI1guCiiB5CO6i6Gr6iyF0mTAk&gclid=Cj0KCQiA2frXBhC_ARIsAPTFcdOHmhO251Vdqm46Gflnlb2foYK_axHaT7EdnsF_oblQBBoz6kJSa94aAsQkEALw_wcB)                                                                                                                                                                                               	|
|                            	| [Stripe](https://stripe.com/gb)                                                                                                                                                                                                                                                                                                                                                                                                                           	|
|                            	| [Brevo](https://www.brevo.com/?utm_source=adwords_brand&utm_medium=lastclick&utm_content=SendinBlue&utm_extension=&utm_term=brevo&utm_matchtype=e&utm_campaign=20034978946&utm_network=g&km_adid=656209990479&km_adposition=&km_device=c&utm_adgroupid=154059591968&gad_source=1&gad_campaignid=20034978946&gbraid=0AAAAADjx0RZ0m1tDrAySz3JS956PLKRkX&gclid=Cj0KCQiA2frXBhC_ARIsAPTFcdMoQX2Y0-tUNGsEwPEgtr7g9DBSuTeHYQXxyMebxE64B90z0RfJ_cYaAuGBEALw_wcB) 	|


##### 1. Clone and install


git clone https://github.com/devildex91/plot_my_path.git
cd plot_my_path

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
npm install


##### 2. Configure environment variables

Create a .env file in the project root and add the following variables:


| Env variable            	| Value                                             	| NOTES                                                                                       	|
|-------------------------	|---------------------------------------------------	|---------------------------------------------------------------------------------------------	|
| DEBUG                   	| True                                              	| Set to False on your deployment                                                             	|
| ALLOWED HOSTS           	| 127.0.0.1,localhost                               	| Set to your URL from deployment when creating Env variables on your deployment of choice    	|
| SECURE_SSL_REDIRECT     	| False                                             	|                                                                                             	|
| GOOGLE_KEY              	| your-google-oauth-client-secret                   	|                                                                                             	|
| CLOUDINARY_URL          	| cloudinary://api_key:api_secret@cloud_name        	|                                                                                             	|
| WEATHER_API_KEY         	| your-visual-crossing-key                          	|                                                                                             	|
| STRIPE_SECRET_KEY       	| sk_test_...                                       	|                                                                                             	|
| STRIPE_PUBLISHABLE_KEY  	| pk_test_...                                       	|                                                                                             	|
| STRIPE_PREMIUM_PRICE_ID 	| price_...                                         	|                                                                                             	|
| STRIPE_WEBHOOK_SECRET   	| whsec_...                                         	|                                                                                             	|
| BREVO_API_KEY           	| your-brevo-key                                    	|                                                                                             	|
| DEFAULT_FROM_EMAIL      	| you@example.com                                   	|                                                                                             	|
| CONTACT_EMAIL           	| you@example.com                                   	|                                                                                             	|
| DATABASE_URL            	| Optional but highly reccommended for deployment   	| Neon was used for this deployment                                                           	|
| DJANGO_SECRET_KEY       	| your django secret key                            	| python -c "from django.core.management.utils import get_random_secret_key as g; print(g())" 	|
|                         	|                                                   	|                                                                                             	|


##### 3. Set up the database

1. python manage.py makemigrations(To check whats being migrated)
2. python manage.py migrate
3. python manage.py createsuperuser and follow the terminal instructions to create a superuser.


- Add destinations and attractions through the admin at /admin/. or create a json of data in the format of the example shown below and run:
-python manage.py loaddata path to your file.json

Examples of data:
countries example:   
{  
    "model": "destinations.country",  
    "fields": {  
      "name": "Japan",  
      "code": "JPN",  
      "continent": "Asia"  
    }  
  },

  destinations example:  
    {    
    "model": "destinations.destination",  
    "fields": {  
      "country": ["Japan"],  
      "name": "Tokyo",  
      "slug": "tokyo",  
      "description": "A hyper-modern metropolis blending neon skyscrapers   with historic Shinto shrines.",  
      "latitude": "35.676200",  
      "longitude": "139.650300",  
      "average_cost_per_day": "150.00"  
    }  
  },  

attractions example:  
  {  
    "model": "destinations.attraction",  
    "fields": {  
      "destination": ["tokyo"],  
      "name": "Senso-ji Temple",  
      "slug": "senso-ji-temple",  
      "description": "Tokyo's oldest and most iconic Buddhist temple located in the heart of Asakusa.",  
      "category": "Historic",  
      "latitude": "35.714800",  
      "longitude": "139.796700",  
      "average_visit_minutes": 90,  
      "entry_cost": "0.00",  
      "rating": "4.70",  
      "opening_time": "06:00:00",  
      "closing_time": "17:00:00"  
    }  
  
  



##### 4. Start the app

Run both servers, each in its own terminal:


##### Terminal 1: frontend (Vite)
npm run dev

##### Terminal 2: backend (Django)
python manage.py runserver


Open http://localhost:8000.

##### Running the tests


python manage.py test

##### Code formatting

black --check .


### Deployment 
- The following steps were used to deploy on render. Please follow the instruction whichever deployment site you choose to use 

The included  Dockerfile builds the frontend, installs the Python dependencies, then on startup runs migrations, collects static files and starts Gunicorn on $PORT. Set these environment variables on your host of choice:

DEBUG=False, DJANGO_SECRET_KEY, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, DATABASE_URL, plus all the keys listed in the .env example above (using live Stripe keys).

Then register your production URLs for Google OAuth (/accounts/google/login/callback/) and the Stripe webhook.
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


