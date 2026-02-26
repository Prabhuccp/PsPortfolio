public with sharing class ContactSummaryHelper {
    @AuraEnabled(cacheable=true)
    public static Map<String, Object> getContactSummary(Id accountId) {
        List<Contact> contacts = [
            SELECT Id, FirstName, LastName, Email
            FROM Contact
            WHERE AccountId = :accountId
        ];
        
        List<String> names = new List<String>();
        for (Contact c : contacts) {
            names.add(c.FirstName + ' ' + c.LastName);
        }

        return new Map<String, Object>{
            'contactCount' => contacts.size(),
            'contactNames' => names
        };
    }
}