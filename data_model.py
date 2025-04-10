# JSON Data structure for flight data
# flight_schema = [
#     {
#         "type": "flight-offer",
#         "id": "1",
#         "source": "GDS",
#         "instantTicketingRequired": false,
#         "nonHomogeneous": false,
#         "oneWay": false,
#         "isUpsellOffer": false,
#         "lastTicketingDate": "2025-03-27",
#         "lastTicketingDateTime": "2025-03-27",
#         "numberOfBookableSeats": 9,
#         "itineraries": [
#             {
#                 "duration": "PT10H30M",
#                 "segments": [
#                     {
#                         "departure": {
#                             "iataCode": "JFK",
#                             "terminal": "7",
#                             "at": "2025-06-01T20:25:00"
#                         },
#                         "arrival": {
#                             "iataCode": "KEF",
#                             "at": "2025-06-02T06:15:00"
#                         },
#                         "carrierCode": "FI",
#                         "number": "614",
#                         "aircraft": {
#                             "code": "76W"
#                         },
#                         "operating": {
#                             "carrierCode": "FI"
#                         },
#                         "duration": "PT5H50M",
#                         "id": "119",
#                         "numberOfStops": 0,
#                         "blacklistedInEU": false
#                     },
#                     {
#                         "departure": {
#                             "iataCode": "KEF",
#                             "at": "2025-06-02T07:40:00"
#                         },
#                         "arrival": {
#                             "iataCode": "LHR",
#                             "terminal": "2",
#                             "at": "2025-06-02T11:55:00"
#                         },
#                         "carrierCode": "FI",
#                         "number": "450",
#                         "aircraft": {
#                             "code": "76W"
#                         },
#                         "operating": {
#                             "carrierCode": "FI"
#                         },
#                         "duration": "PT3H15M",
#                         "id": "120",
#                         "numberOfStops": 0,
#                         "blacklistedInEU": false
#                     }
#                 ]
#             }
#         ],
#         "price": {
#             "currency": "EUR",
#             "total": "344.63",
#             "base": "174.00",
#             "fees": [
#                 {
#                     "amount": "0.00",
#                     "type": "SUPPLIER"
#                 },
#                 {
#                     "amount": "0.00",
#                     "type": "TICKETING"
#                 }
#             ],
#             "grandTotal": "344.63",
#             "additionalServices": [
#                 {
#                     "amount": "90.00",
#                     "type": "CHECKED_BAGS"
#                 }
#             ]
#         },
#         "pricingOptions": {
#             "fareType": [
#                 "PUBLISHED"
#             ],
#             "includedCheckedBagsOnly": false
#         },
#         "validatingAirlineCodes": [
#             "FI"
#         ],
#         "travelerPricings": [
#             {
#                 "travelerId": "1",
#                 "fareOption": "STANDARD",
#                 "travelerType": "ADULT",
#                 "price": {
#                     "currency": "EUR",
#                     "total": "344.63",
#                     "base": "174.00"
#                 },
#                 "fareDetailsBySegment": [
#                     {
#                         "segmentId": "119",
#                         "cabin": "ECONOMY",
#                         "fareBasis": "OP1QUSLT",
#                         "brandedFare": "LIGHT",
#                         "brandedFareLabel": "ECONOMY LIGHT",
#                         "class": "O",
#                         "includedCheckedBags": {
#                             "quantity": 0
#                         },
#                         "includedCabinBags": {
#                             "quantity": 1
#                         },
#                         "amenities": [
#                             {
#                                 "description": "CHECKED BAG UP TO 23KG",
#                                 "isChargeable": true,
#                                 "amenityType": "BAGGAGE",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "ALCOHOLIC DRINK",
#                                 "isChargeable": true,
#                                 "amenityType": "MEAL",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "NON ALCOHOLIC DRINK",
#                                 "isChargeable": false,
#                                 "amenityType": "MEAL",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "MEAL",
#                                 "isChargeable": true,
#                                 "amenityType": "MEAL",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "USB POWER",
#                                 "isChargeable": false,
#                                 "amenityType": "ENTERTAINMENT",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "BASIC SEAT",
#                                 "isChargeable": true,
#                                 "amenityType": "BRANDED_FARES",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             }
#                         ]
#                     },
#                     {
#                         "segmentId": "120",
#                         "cabin": "ECONOMY",
#                         "fareBasis": "OP1QUSLT",
#                         "brandedFare": "LIGHT",
#                         "brandedFareLabel": "ECONOMY LIGHT",
#                         "class": "O",
#                         "includedCheckedBags": {
#                             "quantity": 0
#                         },
#                         "includedCabinBags": {
#                             "quantity": 1
#                         },
#                         "amenities": [
#                             {
#                                 "description": "CHECKED BAG UP TO 23KG",
#                                 "isChargeable": true,
#                                 "amenityType": "BAGGAGE",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "ALCOHOLIC DRINK",
#                                 "isChargeable": true,
#                                 "amenityType": "MEAL",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "NON ALCOHOLIC DRINK",
#                                 "isChargeable": false,
#                                 "amenityType": "MEAL",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "MEAL",
#                                 "isChargeable": true,
#                                 "amenityType": "MEAL",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "USB POWER",
#                                 "isChargeable": false,
#                                 "amenityType": "ENTERTAINMENT",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             },
#                             {
#                                 "description": "BASIC SEAT",
#                                 "isChargeable": true,
#                                 "amenityType": "BRANDED_FARES",
#                                 "amenityProvider": {
#                                     "name": "BrandedFare"
#                                 }
#                             }
#                         ]
#                     }
#                 ]
#             }
#         ]
#     }
# ]

# booking_data = {
#     "type": "flight-order",
#     "id": "eJzTd9f3dg529HUHAAsyAlw%3D",
#     "queuingOfficeId": "NCE4D31SB",
#     "associatedRecords": [
#         {
#             "reference": "KCSAMG",
#             "originSystemCode": "TP",
#             "flightOfferId": "1"
#         },
#         {
#             "reference": "KCSAMG",
#             "creationDate": "2025-03-26T12:51:00",
#             "originSystemCode": "GDS",
#             "flightOfferId": "1"
#         }
#     ],
#     "flightOffers": [
#         {
#             "type": "flight-offer",
#             "id": "1",
#             "source": "GDS",
#             "nonHomogeneous": false,
#             "lastTicketingDate": "2025-03-27",
#             "itineraries": [
#                 {
#                     "segments": [
#                         {
#                             "departure": {
#                                 "iataCode": "ZRH",
#                                 "at": "2025-05-25T18:05:00"
#                             },
#                             "arrival": {
#                                 "iataCode": "LIS",
#                                 "terminal": "1",
#                                 "at": "2025-05-25T20:05:00"
#                             },
#                             "carrierCode": "TP",
#                             "number": "933",
#                             "aircraft": {
#                                 "code": "32N"
#                             },
#                             "duration": "PT3H",
#                             "bookingStatus": "CONFIRMED",
#                             "segmentType": "ACTIVE",
#                             "isFlown": false,
#                             "id": "1",
#                             "numberOfStops": 0,
#                             "co2Emissions": [
#                                 {
#                                     "weight": 136,
#                                     "weightUnit": "KG",
#                                     "cabin": "ECONOMY"
#                                 }
#                             ]
#                         },
#                         {
#                             "departure": {
#                                 "iataCode": "LIS",
#                                 "terminal": "1",
#                                 "at": "2025-05-26T09:00:00"
#                             },
#                             "arrival": {
#                                 "iataCode": "SFO",
#                                 "terminal": "I",
#                                 "at": "2025-05-26T14:00:00"
#                             },
#                             "carrierCode": "TP",
#                             "number": "3335",
#                             "aircraft": {
#                                 "code": "339"
#                             },
#                             "duration": "PT13H",
#                             "bookingStatus": "CONFIRMED",
#                             "segmentType": "ACTIVE",
#                             "isFlown": false,
#                             "id": "2",
#                             "numberOfStops": 0,
#                             "co2Emissions": [
#                                 {
#                                     "weight": 416,
#                                     "weightUnit": "KG",
#                                     "cabin": "ECONOMY"
#                                 }
#                             ]
#                         }
#                     ]
#                 }
#             ],
#             "price": {
#                 "currency": "EUR",
#                 "total": "745.78",
#                 "base": "356.00",
#                 "grandTotal": "745.78"
#             },
#             "pricingOptions": {
#                 "fareType": [
#                     "PUBLISHED"
#                 ]
#             },
#             "validatingAirlineCodes": [
#                 "TP"
#             ],
#             "travelerPricings": [
#                 {
#                     "travelerId": "1",
#                     "travelerType": "ADULT",
#                     "price": {
#                         "currency": "EUR",
#                         "total": "372.89",
#                         "base": "178.00",
#                         "taxes": [
#                             {
#                                 "amount": "36.60",
#                                 "code": "CH"
#                             },
#                             {
#                                 "amount": "2.00",
#                                 "code": "J9"
#                             },
#                             {
#                                 "amount": "8.93",
#                                 "code": "PT"
#                             },
#                             {
#                                 "amount": "21.08",
#                                 "code": "US"
#                             },
#                             {
#                                 "amount": "3.42",
#                                 "code": "XA"
#                             },
#                             {
#                                 "amount": "6.45",
#                                 "code": "XY"
#                             },
#                             {
#                                 "amount": "6.63",
#                                 "code": "YC"
#                             },
#                             {
#                                 "amount": "21.93",
#                                 "code": "YP"
#                             },
#                             {
#                                 "amount": "87.85",
#                                 "code": "YQ"
#                             }
#                         ]
#                     },
#                     "fareDetailsBySegment": [
#                         {
#                             "segmentId": "1",
#                             "cabin": "ECONOMY",
#                             "fareBasis": "EF0DSI09",
#                             "class": "E",
#                             "includedCheckedBags": {
#                                 "quantity": 0
#                             },
#                             "mealServices": [
#                                 {
#                                     "label": "Meal"
#                                 }
#                             ]
#                         },
#                         {
#                             "segmentId": "2",
#                             "cabin": "ECONOMY",
#                             "fareBasis": "EF0DSI09",
#                             "class": "E",
#                             "includedCheckedBags": {
#                                 "quantity": 0
#                             }
#                         }
#                     ]
#                 },
#                 {
#                     "travelerId": "2",
#                     "travelerType": "ADULT",
#                     "price": {
#                         "currency": "EUR",
#                         "total": "372.89",
#                         "base": "178.00",
#                         "taxes": [
#                             {
#                                 "amount": "36.60",
#                                 "code": "CH"
#                             },
#                             {
#                                 "amount": "2.00",
#                                 "code": "J9"
#                             },
#                             {
#                                 "amount": "8.93",
#                                 "code": "PT"
#                             },
#                             {
#                                 "amount": "21.08",
#                                 "code": "US"
#                             },
#                             {
#                                 "amount": "3.42",
#                                 "code": "XA"
#                             },
#                             {
#                                 "amount": "6.45",
#                                 "code": "XY"
#                             },
#                             {
#                                 "amount": "6.63",
#                                 "code": "YC"
#                             },
#                             {
#                                 "amount": "21.93",
#                                 "code": "YP"
#                             },
#                             {
#                                 "amount": "87.85",
#                                 "code": "YQ"
#                             }
#                         ]
#                     },
#                     "fareDetailsBySegment": [
#                         {
#                             "segmentId": "1",
#                             "cabin": "ECONOMY",
#                             "fareBasis": "EF0DSI09",
#                             "class": "E",
#                             "includedCheckedBags": {
#                                 "quantity": 0
#                             },
#                             "mealServices": [
#                                 {
#                                     "label": "Meal"
#                                 }
#                             ]
#                         },
#                         {
#                             "segmentId": "2",
#                             "cabin": "ECONOMY",
#                             "fareBasis": "EF0DSI09",
#                             "class": "E",
#                             "includedCheckedBags": {
#                                 "quantity": 0
#                             }
#                         }
#                     ]
#                 }
#             ]
#         }
#     ],
#     "travelers": [
#         {
#             "id": "1",
#             "dateOfBirth": "1980-07-04",
#             "gender": "MALE",
#             "name": {
#                 "firstName": "MICHAEL",
#                 "lastName": "MOORE"
#             },
#             "documents": [
#                 {
#                     "number": "3805845",
#                     "expiryDate": "2031-08-13",
#                     "issuanceCountry": "ES",
#                     "nationality": "ES",
#                     "documentType": "PASSPORT",
#                     "holder": true
#                 }
#             ],
#             "contact": {
#                 "purpose": "STANDARD",
#                 "phones": [
#                     {
#                         "deviceType": "MOBILE",
#                         "countryCallingCode": "383",
#                         "number": "550481636"
#                     }
#                 ],
#                 "emailAddress": "TYLERWRIGHT@EXAMPLE.COM"
#             }
#         },
#         {
#             "id": "2",
#             "dateOfBirth": "1981-10-06",
#             "gender": "MALE",
#             "name": {
#                 "firstName": "MARK",
#                 "lastName": "SANTOS"
#             },
#             "documents": [
#                 {
#                     "number": "0447797",
#                     "expiryDate": "2032-04-13",
#                     "issuanceCountry": "ES",
#                     "nationality": "ES",
#                     "documentType": "PASSPORT",
#                     "holder": true
#                 }
#             ],
#             "contact": {
#                 "purpose": "STANDARD",
#                 "phones": [
#                     {
#                         "deviceType": "MOBILE",
#                         "countryCallingCode": "353",
#                         "number": "497338366"
#                     }
#                 ],
#                 "emailAddress": "OBROWN@EXAMPLE.NET"
#             }
#         }
#     ],
#     "remarks": {
#         "general": [
#             {
#                 "subType": "GENERAL_MISCELLANEOUS",
#                 "text": "PRICING ENTRY FXP/FF-DISCOUNT/R,P,VC-TP,FC-EUR/P1-2",
#                 "flightOfferIds": [
#                     "1"
#                 ]
#             }
#         ]
#     },
#     "ticketingAgreement": {
#         "option": "CONFIRM"
#     },
#     "contacts": [
#         {
#             "purpose": "STANDARD"
#         }
#     ]
# }

