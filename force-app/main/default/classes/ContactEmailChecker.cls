public with sharing class ContactEmailChecker {

    public class ContactInput {
        @InvocableVariable(label='Contact Id')
        public Id contactId;
        
        @InvocableVariable(label='Email')
        public String email;
    }

    public class ContactOutput {
        @InvocableVariable(label='Updated Description')
        public String updatedDescription;
    }

    @InvocableMethod(label='Check Contact prabhu' description='Update description based on email content')
    public static List<ContactOutput> checkEmail(List<ContactInput> inputs) {
        List<ContactOutput> results = new List<ContactOutput>();

        for (ContactInput input : inputs) {
            ContactOutput output = new ContactOutput();
            if (input.email != null && input.email.containsIgnoreCase('test')) {
                output.updatedDescription = 'Test email detected: auto description set';
            } else {
                output.updatedDescription = 'Regular email';
            }
            results.add(output);
        }

        return results;
    }
}