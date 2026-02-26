public with sharing class AccountCasesController {

    @AuraEnabled(cacheable=true)
    public static List<Case> getCasesByAccountId(Id accountId) {
        if (String.isBlank(accountId) || !String.valueOf(accountId).startsWith('001')) {
            throw new AuraHandledException('Valid Account Id required.');
        }

        return [
            SELECT Id, IsDeleted, MasterRecordId, CaseNumber, ContactId, AccountId, AssetId, ParentId 
            FROM Case 
            WHERE AccountId = :accountId
            LIMIT 10
        ];
    }
}