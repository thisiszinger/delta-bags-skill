# Delta Bags

Delta Bags helps an agent submit Delta's 20-Minute Bag Guarantee request for one or more travelers after an eligible late baggage delivery.

## Language

**20-Minute Bag Guarantee Request**:
A request to Delta for the advertised bonus miles after checked baggage takes more than 20 minutes to reach the baggage carousel on an eligible flight.
_Avoid_: Claim, compensation claim, late-bag claim

**Requesting Traveler**:
The passenger on whose behalf a request is submitted and whose SkyMiles account may receive the award. This defaults to the Agent User but may be another explicitly identified person.
_Avoid_: User, claimant

**Agent User**:
The person directing the agent. The Agent User and Requesting Traveler are often, but not necessarily, the same person.
_Avoid_: Traveler, passenger

**Traveler Profile**:
Private, reusable identity and loyalty information belonging to one Requesting Traveler.
_Avoid_: User profile, account

**Default Traveler**:
The Traveler Profile selected when the Agent User does not name a different Requesting Traveler. It normally represents the Agent User.
_Avoid_: Primary user, account owner

**Saved Companion**:
A Traveler Profile other than the Default Traveler, stored only after the Agent User explicitly asks to retain it for future requests.
_Avoid_: Guest, secondary user

**Affected Flight**:
The flight whose checked-baggage delivery prompted a 20-Minute Bag Guarantee Request.
_Avoid_: Late flight, delayed flight

**Confirmation Number**:
Delta's six-character booking reference required to identify the Affected Flight on the request form.
_Avoid_: Confirmation code, record locator, PNR

**Submission Confirmation**:
Delta's acknowledgement that it received a request. It does not mean Delta approved the request or awarded miles.
_Avoid_: Approval, award confirmation

**Request Outcome**:
The result Delta returns for one request: approved, rejected, duplicate, expired, failed, or unknown. Only Delta's explicit success response establishes an approved outcome.
_Avoid_: Submission status, claim status

**Late-Bag Attestation**:
The Agent User's statement that one Requesting Traveler's checked baggage took more than 20 minutes to reach the carousel. Every traveler in a multi-traveler flow needs a separate attestation.
_Avoid_: Proof, baggage tracking result

**Request Batch**:
A sequence of separate 20-Minute Bag Guarantee Requests for multiple Requesting Travelers on the same Affected Flight.
_Avoid_: Group request, combined request

**Duplicate Ledger**:
A private, rolling 30-day record of request attempts used to warn before repeating a request for the same Requesting Traveler and Affected Flight. It stores flight date, airport pair, Traveler Profile identifier, timestamp, and Request Outcome, but never the Confirmation Number.
_Avoid_: Claim history, submission database
