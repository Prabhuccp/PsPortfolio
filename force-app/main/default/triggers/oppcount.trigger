trigger oppcount on Opportunity (after update, after insert, after delete, after undelete) {
    set<id>accountid = new set<id>();
    
    if(!trigger.isdelete)
    {
        for(opportunity opp : trigger.new)
        {
            accountid.add(opp.accountid);
        }
    }

}