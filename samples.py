# pip install requests

import requests

# Step 1 - Define the constant values.
aadTenant = "https://login.microsoftonline.com/"
aadTenantId = "71035672-b52d-4df1-a6f2-396bd7a6644a"

appId = "34dd30d9-6b63-48f2-8dff-d39823d8d128"
appSecret = "b0affa4b-130c-449f-ae48-c8bb46dfaca6"

fhirEndpoint = "https://healthhub-fhirservice.fhir.azurehealthcareapis.com/"

##########################################################

def getHttpHeader(accessToken):
    return {
        "Authorization": "Bearer " + accessToken,
        "Content-type": "application/json"
    }

def printResourceData(resource):
    resourceType = resource['resourceType']
    itemId = resource['id']
    if (resourceType == "OperationOutcome"):
        print("\t" + resource)
    else:
        itemId = resource['id']
        print("\t" + resourceType + "/" + itemId)

def printResponseResults(response):
    responseAsJson = response.json()

    if (responseAsJson.get('entry') == None):
        # Print the resource type and id of a resource. 
        printResourceData(responseAsJson)
    else:
        # Prints the resource type and ids of all resources under a bundle.
        for item in responseAsJson.get('entry'):
            resource = item['resource']
            printResourceData(resource)

##########################################################

def getAuthToken():
    response = requests.post(
        aadTenant + aadTenantId + '/oauth2/token',
        data={
            'client_id': appId,
            "client_secret": appSecret,
            "grant_type": "client_credentials",
            "resource": fhirEndpoint})
    responseAsJson = response.json()

    if response.status_code != 200:
        print("\tError getting token: " + str(response.status_code))
        return None
    else:
        accessToken = responseAsJson.get('access_token')
        print("\tAAD Access Token acquired: " + accessToken[:50] + "...")
        return accessToken

def postPatient(accessToken):

    # Example of FHIR MedicationRequest: https://www.hl7.org/fhir/R4/medicationrequest0303.json.html

{
  "resourceType": "MedicationRequest",
  "id": "medrx0303",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative with Details</b></p><p><b>id</b>: medrx0303</p><p><b>contained</b>: </p><p><b>identifier</b>: 12345689 (OFFICIAL)</p><p><b>status</b>: active</p><p><b>intent</b>: order</p><p><b>medication</b>: id: med0311; Prednisone 5mg tablet (Product) <span>(Details : {SNOMED CT code '373994007' = 'Prednisone 5mg tablet', given as 'Prednisone 5mg tablet (Product)'})</span></p><p><b>subject</b>: <a>Donald Duck</a></p><p><b>encounter</b>: <a>encounter who leads to this prescription</a></p><p><b>authoredOn</b>: 15/01/2015</p><p><b>requester</b>: <a>Patrick Pump</a></p><p><b>basedOn</b>: <a>CarePlan/gpvisit</a></p><p><b>groupIdentifier</b>: 983939393 (OFFICIAL)</p><p><b>note</b>: Patient told to take with food</p><p><b>dosageInstruction</b>: , , </p><h3>DispenseRequests</h3><table><tr><td>-</td><td><b>ValidityPeriod</b></td><td><b>NumberOfRepeatsAllowed</b></td><td><b>Quantity</b></td><td><b>ExpectedSupplyDuration</b></td><td><b>Performer</b></td></tr><tr><td>*</td><td>15/01/2015 --&gt; 15/01/2016</td><td>1</td><td>51 TAB<span> (Details: http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm code TAB = 'Tablet')</span></td><td>21 days<span> (Details: UCUM code d = 'd')</span></td><td><a>Organization/f001</a></td></tr></table><h3>Substitutions</h3><table><tr><td>-</td><td><b>Allowed[x]</b></td><td><b>Reason</b></td></tr><tr><td>*</td><td>Therapeutic Brand <span>(Details : {http://terminology.hl7.org/CodeSystem/v3-substanceAdminSubstitution code 'TB' = 'therapeutic brand', given as 'Therapeutic Brand'})</span></td><td>formulary policy <span>(Details : {http://terminology.hl7.org/CodeSystem/v3-ActReason code 'FP' = 'formulary policy', given as 'formulary policy'})</span></td></tr></table></div>"
  },
  "contained": [
    {
      "resourceType": "Medication",
      "id": "med0311",
      "code": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "373994007",
            "display": "Prednisone 5mg tablet (Product)"
          }
        ]
      }
    }
  ],
  "identifier": [
    {
      "use": "official",
      "system": "http://www.bmc.nl/portal/prescriptions",
      "value": "12345689"
    }
  ],
  "status": "active",
  "intent": "order",
  "medicationReference": {
    "reference": "#med0311"
  },
  "subject": {
    "reference": "Patient/pat1",
    "display": "Donald Duck"
  },
  "encounter": {
    "reference": "Encounter/f001",
    "display": "encounter who leads to this prescription"
  },
  "authoredOn": "2015-01-15",
  "requester": {
    "reference": "Practitioner/f007",
    "display": "Patrick Pump"
  },
  "basedOn": [
    {
      "reference": "CarePlan/gpvisit"
    }
  ],
  "groupIdentifier": {
    "use": "official",
    "system": "http://www.bmc.nl/portal/prescriptions",
    "value": "983939393"
  },
  "note": [
    {
      "text": "Patient told to take with food"
    }
  ],
  "dosageInstruction": [
    {
      "sequence": 1,
      "text": "Take 4 tablets daily for 7 days starting January 16, 2015",
      "timing": {
        "repeat": {
          "boundsPeriod": {
            "start": "2015-01-16",
            "end": "2015-01-20"
          },
          "frequency": 1,
          "period": 1,
          "periodUnit": "d"
        }
      },
      "route": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "26643006",
            "display": "Oral Route"
          }
        ]
      },
      "method": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "421521009",
            "display": "Swallow - dosing instruction imperative (qualifier value)"
          }
        ]
      },
      "doseAndRate": [
        {
          "type": {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/dose-rate-type",
                "code": "ordered",
                "display": "Ordered"
              }
            ]
          },
          "doseQuantity": {
            "value": 4,
            "unit": "TAB",
            "system": "http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm",
            "code": "TAB"
          }
        }
      ]
    },
    {
      "sequence": 2,
      "text": "Take 2 tablets daily for 7 days starting January 23, 2015",
      "timing": {
        "repeat": {
          "boundsPeriod": {
            "start": "2015-01-23",
            "end": "2015-01-30"
          },
          "frequency": 1,
          "period": 1,
          "periodUnit": "d"
        }
      },
      "route": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "26643006",
            "display": "Oral Route"
          }
        ]
      },
      "method": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "421521009",
            "display": "Swallow - dosing instruction imperative (qualifier value)"
          }
        ]
      },
      "doseAndRate": [
        {
          "type": {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/dose-rate-type",
                "code": "ordered",
                "display": "Ordered"
              }
            ]
          },
          "doseQuantity": {
            "value": 2,
            "unit": "TAB",
            "system": "http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm",
            "code": "TAB"
          }
        }
      ]
    },
    {
      "sequence": 3,
      "text": "Take 1 tablets daily for 7 days starting January 31, 2015",
      "timing": {
        "repeat": {
          "boundsPeriod": {
            "start": "2015-01-31",
            "end": "2015-02-06"
          },
          "frequency": 1,
          "period": 1,
          "periodUnit": "d"
        }
      },
      "route": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "26643006",
            "display": "Oral Route"
          }
        ]
      },
      "method": {
        "coding": [
          {
            "system": "http://snomed.info/sct",
            "code": "421521009",
            "display": "Swallow - dosing instruction imperative (qualifier value)"
          }
        ]
      },
      "doseAndRate": [
        {
          "type": {
            "coding": [
              {
                "system": "http://terminology.hl7.org/CodeSystem/dose-rate-type",
                "code": "ordered",
                "display": "Ordered"
              }
            ]
          },
          "doseQuantity": {
            "value": 1,
            "unit": "TAB",
            "system": "http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm",
            "code": "TAB"
          }
        }
      ]
    }
  ],
  "dispenseRequest": {
    "validityPeriod": {
      "start": "2015-01-15",
      "end": "2016-01-15"
    },
    "numberOfRepeatsAllowed": 1,
    "quantity": {
      "value": 51,
      "unit": "TAB",
      "system": "http://terminology.hl7.org/CodeSystem/v3-orderableDrugForm",
      "code": "TAB"
    },
    "expectedSupplyDuration": {
      "value": 21,
      "unit": "days",
      "system": "http://unitsofmeasure.org",
      "code": "d"
    },
    "performer": {
      "reference": "Organization/f001"
    }
  },
  "substitution": {
    "allowedCodeableConcept": {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-substanceAdminSubstitution",
          "code": "TB",
          "display": "Therapeutic Brand"
        }
      ]
    },
    "reason": {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/v3-ActReason",
          "code": "FP",
          "display": "formulary policy"
        }
      ]
    }
  }
}

    # Example of FHIR Patient: https://www.hl7.org/fhir/patient-example.json.html

    patientData = {
        "resourceType" : "Patient",
        "active" : True,
        "name" : [{
            "use" : "official",
            "family" : "LastName",
            "given" : ["FirstName", "MiddleName"]
        }],
        "telecom" : [
        {
            "system" : "phone",
            "value" : "(11) 99988-7766",
            "use" : "mobile",
            "rank" : 1
        }],
        "gender" : "male",
        "birthDate" : "1974-12-25",
        "address" : [{
            "use" : "home",
            "type" : "both",
            "text" : "534 Erewhon St PeasantVille, Rainbow, Vic  3999",
            "line" : ["534 Erewhon St"],
            "city" : "PleasantVille",
            "district" : "Rainbow",
            "state" : "Vic",
            "postalCode" : "3999",
            "period" : {
            "start" : "1974-12-25"
            }
        }]
    }

    response = requests.post(
        url= fhirEndpoint + 'Patient',
        json= patientData,
        headers= getHttpHeader(accessToken))
    responseAsJson = response.json()
    
    if response.status_code == 200 or response.status_code == 201:
        resourceId = responseAsJson.get('id')
        print("\tPatient ingested: " + resourceId + ". HTTP " + str(response.status_code))
        return resourceId
    else:
        print("\tError persisting patient: " + str(response.status_code))
        return None

def postPractitioner(accessToken):

    # Example of FHIR Practitioner: https://www.hl7.org/fhir/practitioner-example.json.html

    practitionerData = {
        "resourceType": "Practitioner",
        "active": True,
        "name": [
            {
            "family": "Smith",
            "given": ["John"]
            }
        ],
        "gender": "male",
        "birthDate": "1975-05-15",
        "address": [
            {
            "use": "home",
            "line": ["123 Main Street"],
            "city": "Anytown",
            "state": "CA",
            "postalCode": "12345"
            }
        ],
        "telecom": [
            {
            "system": "phone",
            "value": "555-555-5555"
            },
            {
            "system": "email",
            "value": "john.smith@example.com"
            }
        ],
        "qualification": [
            {
            "code": {
                "coding": [
                {
                    "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                    "code": "Physician"
                }
                ],
                "text": "Physician"
            },
            "period": {
                "start": "2000-01-01"
            }
            }
        ]
    }

    response = requests.post(
        url= fhirEndpoint + 'Practitioner',
        json= practitionerData,
        headers= getHttpHeader(accessToken))
    responseAsJson = response.json()
    
    if response.status_code == 200 or response.status_code == 201:
        resourceId = responseAsJson.get('id')
        print("\tPractitioner ingested: " + resourceId + ". HTTP " + str(response.status_code))
        return resourceId
    else:
        print("\tError persisting practitioner: " + str(response.status_code))
        return None
    
def postAppointment(patientId, practitionerId, accessToken):

    # https://hl7.org/fhir/R4/appointment-example.json.html

    appointmentData = {
        "resourceType": "Appointment",
        "status": "booked",
        "description": "Follow-up appointment with Dr. Smith",
        "start": "2023-09-20T10:00:00-04:00",
        "end": "2023-09-20T11:00:00-04:00",
        "participant": [
            {
            "actor": {
                "reference": "Practitioner/" + practitionerId
            },
            "status": "accepted",
            "type": [
                {
                "coding": [
                    {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                    "code": "ATND"
                    }
                ],
                "text": "Attendee"
                }
            ]
            },
            {
            "actor": {
                "reference": "Patient/" + patientId
            },
            "status": "accepted",
            "type": [
                {
                "coding": [
                    {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                    "code": "PAT"
                    }
                ],
                "text": "Patient"
                }
            ]
            }
        ]
    }

    response = requests.post(
        url= fhirEndpoint + 'Appointment',
        json= appointmentData,
        headers= getHttpHeader(accessToken))
    responseAsJson = response.json()
    
    if response.status_code == 200 or response.status_code == 201:
        resourceId = responseAsJson.get('id')
        print("\tAppointment ingested: " + resourceId + ". HTTP " + str(response.status_code))
        return resourceId
    else:
        print("\tError persisting appointment: " + str(response.status_code))
        return None


def printPatientInfo(patientId, accessToken):

    # GET htts://<fhir endpoint>/Patient/<patientId>

    baseUrl = fhirEndpoint + 'Patient/' + patientId

    response = requests.get(
        baseUrl,
        headers= getHttpHeader(accessToken))
    
    if response.status_code == 200 or response.status_code == 201:
        printResponseResults(response)
    else:
        print("\tError getting pattient data: " + str(response.status_code))

def printAllAppointmentsAssignedToPatient(patientId, accessToken):

    # GET htts://<fhir endpoint>/Appointment?actor=Patient/<patientId>

    baseUrl = fhirEndpoint + 'Appointment'
    queryParams = { 'actor' : "Patient/" + patientId }

    response = requests.get(
        baseUrl,
        params= queryParams,
        headers= getHttpHeader(accessToken))
    
    if response.status_code == 200 or response.status_code == 201:
        printResponseResults(response)
    else:
        print("\tError getting appointments: " + str(response.status_code))

##########################################################

if __name__ == '__main__':
    # Step 2 - Acquire authentication token
    print("Acquire authentication token for secure communication.")
    accessToken = getAuthToken()
    if accessToken == None:
        exit()

    # Step 3 - Insert Patient
    print("Persist Patient data.")
    patientId = postPatient(accessToken)
    if patientId == None:
        exit()

    # Step 4 - Insert Practitioner (Doctor)
    print("Persist Practitioner data.")
    practitionerId = postPractitioner(accessToken)
    if practitionerId == None:
        exit()
    
    # Step 5 - Insert Appointments
    print("Insert multiple appointments using Patient and Practitioner IDs.")
    appointmentId1 = postAppointment(patientId, practitionerId, accessToken)
    if appointmentId1 == None:
        exit()

    appointmentId2 = postAppointment(patientId, practitionerId, accessToken)
    if appointmentId2 == None:
        exit()  

    appointmentId3 = postAppointment(patientId, practitionerId, accessToken)
    if appointmentId3 == None:
        exit()

    # Step 6 - Print Patient info
    print("Query Patient's data.")
    printPatientInfo(patientId, accessToken)

    # Step 7 - Print all appointments assigned to a Patient
    print("Query all Appointments assigned to a Patient.")
    printAllAppointmentsAssignedToPatient(patientId, accessToken)