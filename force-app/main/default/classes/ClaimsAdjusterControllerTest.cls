@isTest
private class ClaimsAdjusterControllerTest {
    @testSetup
    static void setupTestData() {
        // Create a real active test user
        Profile p = [SELECT Id FROM Profile WHERE Name = 'Standard User' LIMIT 1];
        User u = new User(
            FirstName = 'Test',
            LastName = 'User',
            Alias = 'tuser',
            Username = 'testuser1234343@example.com.test',
            Email = 'testuser123@example.com',
            TimeZoneSidKey = 'America/Los_Angeles',
            LocaleSidKey = 'en_US',
            EmailEncodingKey = 'UTF-8',
            LanguageLocaleKey = 'en_US',
            ProfileId = p.Id
        );
        User thisUser = [SELECT Id FROM User WHERE Id = :UserInfo.getUserId()];
        System.runAs(thisUser) {
            insert u;
            PermissionSet ps = [SELECT Id FROM PermissionSet WHERE Name = 'Insurance_Full_Access' LIMIT 1];
            insert new PermissionSetAssignment(AssigneeId = u.Id, PermissionSetId = ps.Id);
        }

        // Query Policy__c RecordType
        Id policyRT = Schema.SObjectType.Policy__c.getRecordTypeInfosByDeveloperName()
            .get('Auto')
            .getRecordTypeId();
        Id claimRT = Schema.SObjectType.Claim__c.getRecordTypeInfosByDeveloperName()
            .get('Accident')
            .getRecordTypeId();

        // Create Contact owned by same user
        Contact con = new Contact(
            FirstName = 'John',
            LastName = 'Doe',
            OwnerId = u.Id
        );
        insert con;

        // Create Policy owned by same user
        Policy__c policy = new Policy__c(
            Customer__c = con.Id,
            RecordTypeId = policyRT,
            OwnerId = u.Id,
            Policy_Type__c = 'Auto',
            VIN__c = '1A903284375893532'
        );
        insert policy;

        // Create Claim owned by same user
        Claim__c claim = new Claim__c(
            Policy__c = policy.Id,
            RecordTypeId = claimRT,
            Claim_Amount__c = 5000,
            Approval_Status__c = 'New',
            Date_of_Loss__c = Date.today().addDays(-10),
            OwnerId = u.Id
        );
        insert claim;
        System.debug('Claim inserted: ' + claim.Id);
    }

    @isTest
    static void testGetAssignedClaims() {
        User u = [SELECT Id FROM User WHERE Username = 'testuser1234343@example.com.test' LIMIT 1];
        Claim__c c = [SELECT Id, OwnerId FROM Claim__c LIMIT 1];
        c.OwnerId = u.Id;
        update c;

        System.runAs(u) {
            Test.startTest();
            List<ClaimsAdjusterController.ClaimWrapper> results =
                ClaimsAdjusterController.getAssignedClaims();
            System.debug('Result is: ' + results);
            Test.stopTest();

            ClaimsAdjusterController.ClaimWrapper wrap = results[0];
            System.assertNotEquals(null, wrap.claimId);
            System.assertNotEquals(null, wrap.claimNumber);
            System.assertEquals('New', wrap.status);
            System.assertEquals(5000, wrap.claimAmount);
            System.assert(wrap.policyHolderName.contains('John'));
            System.assertNotEquals('Unknown', wrap.policyType);
        }
    }

    @isTest
    static void testEdgeCases() {
        User u = [SELECT Id FROM User WHERE Username = 'testuser1234343@example.com.test' LIMIT 1];
        System.runAs(u) {
            Claim__c c = new Claim__c(Approval_Status__c = 'Draft');
            ClaimsAdjusterController.ClaimWrapper wrap = new ClaimsAdjusterController.ClaimWrapper(c, null, null);
            System.assertEquals('Unknown', wrap.policyType);
            System.assertEquals('', wrap.policyHolderName);
            System.assertEquals(0, wrap.daysOpen);
        }
    }
}
