import { LightningElement, api, wire } from 'lwc';
import getContactSummary from '@salesforce/apex/ContactSummaryHelper.getContactSummary';

export default class ContactSummary extends LightningElement {
    @api accountId;

    contactCount;
    contactNames = [];
    error;

    @wire(getContactSummary, { accountId: '$accountId' })
    wiredSummary({ error, data }) {
        if (data) {
            this.contactCount = data.contactCount;
            this.contactNames = data.contactNames;
            this.error = undefined;
        } else if (error) {
            this.error = 'Error fetching contact summary.';
            this.contactCount = 0;
            this.contactNames = [];
        }
    }
}