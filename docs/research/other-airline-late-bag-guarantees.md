# Other-Airline Late-Bag Guarantees

Research checked: 2026-08-15. Sources are limited to airline-owned pages and airline-issued material. No form was submitted and no personal data was entered.

## Decision

Keep the initial skill **Delta-specific** and keep the repository name `delta-bags-skill`.

Alaska has a genuinely comparable 20-minute, fixed-benefit guarantee, but its current terms require the traveler to claim it **in person at the arrival airport**. There is no repeatable online request for an agent to submit. Volaris has a current fixed-benefit baggage guarantee with a self-service report, but it applies when a bag does not arrive on the passenger's flight (and, for an enhanced U.S. offer, after 15 hours), not to a slightly late carousel delivery. That is a different mishandled-baggage workflow.

The practical product boundary is therefore:

- Build the complete Delta workflow now.
- Leave an internal seam for airline-specific policy and submission adapters.
- Do not rename the project to `late-bags` merely because adjacent guarantees exist.
- Consider a future Alaska **airport reminder/guidance** adapter and a separate Volaris **mishandled-bag** adapter only if users request them. Neither can reuse Delta's browser-submission workflow as-is.

## Current programs with fixed benefits

| Airline | Trigger | Fixed benefit | Claim channel | Reusable with Delta automation? |
| --- | --- | --- | --- | --- |
| Delta | Bag reaches carousel more than 20 minutes after gate arrival on an eligible flight | 2,500 SkyMiles | Online form within 2 hours | Yes; this is the target workflow |
| Alaska | Bag is not at baggage claim within 20 minutes of gate arrival | Choice of $25 discount code or 2,500 Atmos Rewards points | **In person** at arrival-airport baggage office within 2 hours | No; an agent cannot complete the decisive step remotely |
| Volaris | Bag does not arrive on the same flight; separate enhanced offer after 15 hours on eligible U.S. travel | 1,000 MXN / USD 80 voucher; enhanced U.S. offer 4,500 MXN / USD 240 voucher | Self-service mishandled-bag report or airport agent; email follow-up | Only as a substantially different adapter |

Delta's details are covered separately in [Delta 20-Minute Bag Guarantee](./delta-bags-on-time-policy.md).

### Alaska Airlines

Alaska's current [delayed/damaged/missing baggage page](https://www.alaskaair.com/content/travel-info/baggage/baggage-claim/delayed-damaged-missing) says that a bag not at baggage claim within 20 minutes of the arrival of an Alaska or Hawaiian flight at the gate earns the traveler a choice of a **$25 discount code** or **2,500 Atmos Rewards bonus points**.

The operational terms on that same page are more specific:

- The guarantee must be claimed from a customer-service agent **in person at the arrival airport within two hours**.
- Its legal scope lists flights operated by Alaska (0001-1999), Horizon (2000-2999), and SkyWest (3000-3499), excluding Dutch Harbor and international flights requiring customs clearance.
- Odd-size/oversize-claim items are excluded, including checked pets, golf clubs, skis, surfboards, assistive devices, and firearms.
- Non-revenue space-available travelers and industry-discount travelers are excluded.
- Alaska may suspend the guarantee for baggage-system malfunctions, severe weather, or other conditions outside its control.
- The limit is one guarantee per qualified traveler per flight, regardless of bag count.
- Points should post within three days. The discount code has separate purchase and expiration terms and cannot be redeemed for cash.

#### Hawaiian ambiguity

The current consumer-facing paragraph says “Alaska or Hawaiian Airlines flight,” and the page title covers both brands. The legal terms immediately below it enumerate only Alaska, Horizon, and SkyWest flight-number ranges and do not enumerate Hawaiian-operated flights. An implementation should not infer Hawaiian eligibility until the live terms become unambiguous or an Alaska/Hawaiian agent confirms it for the particular flight.

#### Submission mechanics and automation fit

There is no public form for making the guarantee request. The traveler must speak to an airport agent within the two-hour window. Alaska links to a JavaScript-protected [voucher redemption page](https://www.alaskaair.com/ondemanddiscount/ssl/discountcodeclaim.aspx?campaignid=ECBSG24), but that happens only after the airport agent issues the guarantee voucher. No request-form fields or authentication requirements are published because the decisive validation is in person.

This makes Alaska useful as an agent-assisted reminder—resolve the flight, verify the live policy, alert the user at 20 minutes, and direct them to the baggage office—but not as a remote browser-automation adapter. It would also require a different success contract: “traveler obtained a voucher,” not “agent submitted the request.”

### Volaris

Volaris's current [Baggage Guarantee](https://cms.volaris.com/en/travel-info/baggage-policy/baggage-guarantee/) is fixed-benefit and digitally initiated, but it solves a more serious problem than Delta's policy: the checked bag did **not arrive on the same flight**.

For travel within Mexico and to/from Central and South America:

- A properly tagged checked bag that fails to arrive on the passenger's flight qualifies for an electronic voucher of **1,000 MXN or USD 80**, based on booking currency.
- The traveler must file a report through Volaris's linked third-party self-service module or speak to an airport agent **before leaving baggage claim**.
- Volaris says it sends the voucher number to the email in the report within 72 hours. If it does not, the traveler must contact Volaris with the reservation code.
- The guarantee is one incident per traveler even when several bags are delayed.
- The voucher is personal, non-transferable, non-cash, and valid for purchases for 180 days; the page says it becomes effective 72 hours after arrival.
- The guarantee excludes last-minute travelers and baggage delays caused by security restrictions.

For flights to/from the United States, Volaris describes the same 1,000 MXN / USD 80 same-flight guarantee and a separate enhanced offer for customers who paid a checked-bag charge: if the bag is not delivered to the traveler or collected within **15 hours** after arrival on a Volaris-operated flight, the traveler may be offered an electronic voucher of **4,500 MXN or USD 240**, described as approximately 150% of the bag-transport charge. The traveler must accept the offer by email. The enhanced offer does not apply when customs clearance remains, the traveler failed to collect a properly transported bag, separate reservations caused the missed recheck, the traveler agreed to send the bag on another flight, no bag charge was paid, or no delayed/lost-bag report was filed. It is also unavailable if the traveler requested or received a delayed/lost-bag refund.

#### Submission mechanics and automation fit

The airline page exposes the channel and process but not the complete third-party form schema or its authentication behavior. Observable requirements include a registered bag tag/receipt, a baggage report, the traveler's email, and a reservation code for follow-up. Because the triggering fact is that a bag is missing from the flight—not that it reached a carousel a few minutes late—the workflow must create and manage a mishandled-bag case, wait for email, and potentially handle delivery and expenses. Reusing Delta's seven-field, immediate-result form would be unsafe.

Volaris is a credible future adapter for a broader baggage-assistance product, but it is not a reason to generalize this skill before the Delta flow exists.

## Ordinary delayed/lost-baggage policies, not comparable guarantees

The other major U.S. and Canadian airlines reviewed publish mishandled-baggage reporting, fee refunds, and receipt-based reimbursement. Those are valuable passenger-rights workflows, but they are not short carousel-time guarantees with a fixed goodwill award:

- [American Airlines](https://www.aa.com/i18n/travel-info/baggage/delayed-or-damaged-baggage.jsp) supports an online delayed-bag report (last name plus confirmation code or bag-tag number), a 13-character case ID, reimbursement of reasonable necessities with receipts, and a later property claim. Its [refund FAQ](https://www.aa.com/web/i18n/customer-service/faqs/customer-service-faqs.html) applies 12/15/30-hour thresholds to bag-fee refunds, not a fixed bonus for slow carousel delivery.
- [United Airlines](https://www.united.com/en/us/baggage/bag-help) routes customers through delayed-bag case management. Its [claim-status page](https://www.united.com/en/us/claimform/checkstatus/) links separate forms for interim expenses and bags missing more than five days and accepts a confirmation number or file reference plus last name. No short delivery-time award is published.
- [Southwest Airlines](https://support.southwest.com/helpcenter/s/pathway/a1F5G00000cLOrOUAW/my-baggage-is-missing-delayed-or-damaged) asks travelers to create a mishandled-bag report in person, by airport QR code, or online, generally within four hours for domestic travel. Its [Customer Service Commitment](https://www.southwest.com/swa-resources/pdfs/corporate-commitments/customer-service-commitment.pdf) promises reasonable efforts to return delayed bags within 24 hours and considers documented reasonable expenses; it does not promise a fixed benefit for a brief carousel delay.
- [JetBlue](https://www.jetblue.com/help/bag-claims) offers online delayed/damaged-bag reports within four hours and receipt upload for reasonable essentials. Its [Customer Service Plan](https://www.jetblue.com/customer-assurance/customer-service-plan) promises reasonable efforts to return mishandled bags within 24 hours and receipt-based reimbursement, not a timed carousel award.
- [Air Canada](https://www.aircanada.com/ca/en/aco/home/legal/air-canada-customer-service-plan.html) says it will make reasonable efforts to return a delayed bag within 24 hours, refund the bag fee, and reimburse reasonable interim expenses supported by proof. There is no fixed benefit for missing a short carousel target.
- [WestJet](https://www.westjet.com/en-pr/interruptions) requires a delayed-bag report, states recommended receipt-based interim-expense amounts, and handles lost/damaged-bag compensation. Its [reimbursement form](https://www.westjet.com/en-co/baggage/lost-delayed-damaged/submit-expenses) requires a baggage-report number, reservation and flight details, expense total, and receipts; this is not a fixed late-carousel guarantee.
- [Porter](https://www.flyporter.com/en-us/travel-information/baggage/delayed-or-damaged-baggage) refunds a paid bag fee when the bag does not arrive on the same flight, reimburses supported necessities, and treats bags as lost after 21 days. Its current page does not state the former 30-minute fixed-award guarantee described below.

These policies should not be folded into a “late bags” skill without changing the product from quick guarantee requests into general mishandled-baggage case management.

## Historical or no-longer-current short-time guarantee

### Porter Airlines' 2013 program

An airline-issued [Porter press release from July 2013](https://www.newswire.ca/news-releases/porter-introduces-30-minute-baggage-delivery-guarantee-updates-policies-fees-512681531.html) introduced a close analogue: all checked bags were to reach baggage claim within **30 minutes of gate arrival**, or the passenger received a **$25 voucher** for future Porter travel within six months. The traveler had to report the delay to an on-site Porter agent within one hour. It was limited to one voucher per passenger and excluded oversize and special-handling items.

Porter's current [delayed-baggage page](https://www.flyporter.com/en-us/travel-information/baggage/delayed-or-damaged-baggage) now documents same-flight bag-fee refunds and receipt-based expense reimbursement, but no 30-minute guarantee or $25 late-delivery voucher. The 2013 program should therefore be treated as historical/no longer documented as current, not as an implementable adapter.

## Product implications

The reusable part is not a universal form. It is a small orchestration kernel:

1. Resolve the airline, affected flight, travelers, and checked-bag attestation.
2. Load and verify that airline's live policy.
3. Dispatch to an airline-specific workflow with its own deadline, evidence, channel, fields, and outcome semantics.

Today, only Delta combines all three properties needed for this repository's intended magical flow: a short objective delivery threshold, a fixed benefit, and a remote self-service request that an agent can complete. Alaska has the first two but not the third. Volaris has a fixed benefit and online reporting, but for a different incident class. That evidence favors a Delta-specific public identity now with adapter-ready internals, rather than a prematurely generic name and promise.
