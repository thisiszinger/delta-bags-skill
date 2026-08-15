# Delta 20-Minute Bag Guarantee

Research checked: 2026-08-15. Sources are limited to official Delta pages. No claim was submitted.

## Current operational answer

A passenger may request 2,500 bonus SkyMiles when a checked bag takes **more than 20 minutes** to reach the baggage carousel after an eligible domestic Delta flight. The request should be made **after the flight and within two hours of arrival**. Delta's live claim page and current baggage FAQ both state the two-hour deadline, although an older Delta-hosted terms page still says three days. An agent should therefore treat two hours as the hard operational cutoff and re-read the live claim page immediately before attempting a submission.

## Eligibility

Delta's [live claim page](https://www.delta.com/bag-guarantee) and [Baggage FAQs](https://www.delta.com/us/en/baggage/additional-baggage-information/baggage-faqs) establish these requirements:

- The delayed item must be a checked bag on a domestic flight within the 50 United States or Puerto Rico.
- The qualifying flight must be marketed and operated by Delta Air Lines or a Delta Connection carrier.
- An itinerary containing codeshare segments may qualify only when its final leg is both marketed and operated by Delta or Delta Connection.
- The passenger must be a SkyMiles member in good standing at the time of travel and when the miles are awarded, and the SkyMiles number must have been included on the reservation.
- The ticket must be a paid ticket at a published fare.
- If any one of several checked bags is late, the passenger may qualify, but Delta limits the offer to one request per passenger per outbound or return travel, regardless of the number of checked bags. Requests for multiple trips must be submitted separately.

## Timing and deadline

The [live claim page](https://www.delta.com/bag-guarantee) currently says to submit only after the flight and no later than two hours after arrival. Its current terms likewise say the request must be submitted through `delta.com/bagsontime` within two hours of completion of the affected flight. The [Baggage FAQs](https://www.delta.com/us/en/baggage/additional-baggage-information/baggage-faqs) repeat both "two hours" and "120 minutes."

Delta's currently rendered claim-page terms and FAQ define the bag-delivery interval as the time from the aircraft's **arrival at the gate** to delivery of the bag to the baggage-claim belt/carousel. Delta's baggage-tracking system controls the measurement where it is available. A passenger's own timer can prompt a request but is not the governing measurement stated by Delta.

### Conflict in Delta-hosted material

An [older static Delta terms page](https://www.delta.com/utils/bagsontime/bagsOnTimeStaticText/bagsOnTimeT%26C.html) remains publicly accessible and says:

- requests may be submitted within **three days** of the flight; and
- measurement begins at **aircraft door open**, rather than arrival at the gate.

That Delta-hosted static page conflicts with the canonical page as rendered live and with the current FAQ. For automation, use the stricter **two-hour** deadline, do not promise eligibility based on a personal door-open timer, and re-check the canonical live terms at execution time because Delta reserves the right to modify the guarantee without notice.

## Exclusions and Delta discretion

The [live claim-page terms](https://www.delta.com/bag-guarantee) exclude:

- oversize and overweight baggage;
- special items;
- travel using employee pass privileges; and
- employees of other airlines traveling on industry-discounted tickets.

Delta may suspend the guarantee without prior notice for airport baggage-system malfunctions, severe weather, or other conditions outside its control that prevent timely delivery. It may deny fraudulent, suspicious, or ineligible claims, and says other restrictions may apply. Delta also reserves the right to terminate or modify the guarantee without prior notice.

## Award and fulfillment

For each qualifying baggage-delay occurrence, Delta offers a one-time award of **2,500 bonus miles**. The miles do not count toward Medallion qualification or Million Miler status. According to the [claim page](https://www.delta.com/bag-guarantee) and [FAQ](https://www.delta.com/us/en/baggage/additional-baggage-information/baggage-faqs), the miles appear on the member's SkyMiles statement, and the passenger should allow up to two weeks after the request for the credit to appear.

The cited policy pages do not describe a separate claim-status tracker or guarantee that submission results in an award. A safe agent workflow should preserve the submission confirmation, avoid asserting approval, and advise the user to check their SkyMiles statement after the stated two-week window.

## Live form inspection

The live form was inspected read-only on 2026-08-15 while visibly signed out. No personal data was entered and no request was submitted. The form says all fields are required and presents:

| Label | Control ID | Client-side constraint observed in Delta's current app |
| --- | --- | --- |
| First Name | `first_name` | Letters and spaces; maximum 25 characters |
| Last Name | `last_name` | Letters and spaces; maximum 40 characters |
| SkyMiles Number | `skymiles_number` | Exactly 10 digits |
| Date of Departure | `departure_date` | Required dropdown |
| Departure City | `departureCity` | Three-letter airport code selected through predictive search |
| Arrival City | `arrivalCity` | Three-letter airport code selected through predictive search |
| Confirmation Number | `confirmation_number` | Exactly 6 alphanumeric characters |

The date dropdown exposed the current date and the previous three calendar dates. That UI range does **not** extend the policy deadline: the current page terms, FAQ, and Delta's own late-submission response message all enforce 120 minutes after arrival.

### Authentication and CAPTCHA

The complete form loaded and was usable while Delta's header displayed **Log in**, so a user login is not required. Delta's current client sends the submission with `Authorization: GUEST` for a signed-out visitor; when an existing Delta login is detected, the same app instead obtains and sends a bearer token. Inspection of the current bundle found no form-prefill or alternate-field branch for signed-in users, so the implementation indicates that login changes request authorization rather than the seven form fields. This signed-in behavior is an inference from Delta's current client code, not a direct signed-in rendering test.

No visible CAPTCHA appeared, and the loaded application bundles contained no reCAPTCHA, hCaptcha, or Turnstile integration. Because the request was not submitted, this does not rule out a conditional server-side bot or risk challenge. The page does load anti-fraud/anti-bot telemetry.

## Submission flow and result states

The current Delta client validates the seven fields, builds the request, and sends a `POST` to Delta's `processDelayedBagCompensation` service. This call was identified from Delta's public app configuration and client code but was **not** executed during research.

Delta's current [result-message data](https://www.delta.com/content/www/en_US/baggage/guarantee-messages.baggagedata.json) defines these outcomes:

- **Approved:** “Claim Successful”; the page says the request succeeded and miles have been posted, links to SkyMiles Account Activity, and offers **Submit Another Request**.
- **Not eligible:** bags arrived on time (`1998`), no checked bags were associated with the reservation (`1011`), or the airports are ineligible (`2001`).
- **Input or lookup problem:** itinerary details do not match (`1005`, `1004`, `07641`, or `V018`), the SkyMiles account is invalid, or the request is a duplicate.
- **Deadline:** requests outside 120 minutes receive code `1010`.
- **Operational or technical failure:** Delta defines a temporary irregular-operations message and generic processing-error messages.

The approved result copy says miles have been posted, while the public policy says to allow up to two weeks for credit. An agent should report the exact result Delta returned, preserve the confirmation, and distinguish **submitted** from **approved** unless the result explicitly says the claim was successful.

## Privacy of form values

A SkyMiles number alone does not provide account access; Delta requires a password and may require additional verification for sensitive account operations. It is still a persistent customer identifier, but storing it in a private plaintext Traveler Profile is a materially lower risk than storing a password.

A confirmation number is different. Delta's public My Trips lookup accepts a confirmation number plus the traveler's first and last name without requiring login. Delta's [privacy policy](https://www.delta.com/us/en/legal/privacy-and-security) explicitly says booking references should remain confidential because disclosure may allow access to booking details. Once a trip is located, Delta documents My Trips actions that include seat selection, flight changes, and cancellation. A confirmation number can remain consequential after one flight lands when the same reservation contains a connection or return flight.

The skill should therefore treat the confirmation number as trip-private data: use it for the request, avoid persisting it in a Traveler Profile or submission ledger, and do not echo it by default. If the product intentionally displays it for final review, that should be an explicit privacy tradeoff rather than an assumption that the value is harmless.

## Official sources

- [20-Minute Bag Guarantee and claim form](https://www.delta.com/bag-guarantee) — canonical live claim page, eligibility terms, exclusions, award, and fulfillment.
- [Baggage FAQs: 20 Minute Bag Guarantee](https://www.delta.com/us/en/baggage/additional-baggage-information/baggage-faqs) — calculation method, multiple-bag rule, two-hour deadline, and fulfillment period.
- [Legacy static Bags on Time terms](https://www.delta.com/utils/bagsontime/bagsOnTimeStaticText/bagsOnTimeT%26C.html) — Delta-hosted older language that conflicts on deadline and timing start point.
- [Live form content and field definitions](https://www.delta.com/content/www/en_US/baggage/guarantee.baggagedata.json) — labels, validation messages, and current terms rendered by the app.
- [Live form result messages](https://www.delta.com/content/www/en_US/baggage/guarantee-messages.baggagedata.json) — approval, ineligibility, mismatch, duplicate, deadline, and technical result states.
- [Baggage application configuration](https://www.delta.com/content/www/en_US/config/baggage-config.commonconfig.json) — current submission service and signed-in authentication configuration.
- [Delta privacy and security policy](https://www.delta.com/us/en/legal/privacy-and-security) — confidentiality warning for booking references and multi-passenger bookings.
- [My Trips lookup](https://www.delta.com/my-trips/search) — public lookup requiring confirmation number and traveler name.
