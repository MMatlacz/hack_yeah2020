import { API_URL } from 'react-native-dotenv'


class HelpRequestsService {
    api_url: string;
    user: object;

    constructor(user: object) {
        this.user = user;
        this.api_url = API_URL;

        this.getHelpRequests = this.getHelpRequests.bind(this);
        this.getHelpRequest = this.getHelpRequest.bind(this);
        this.assignForHelp = this.assignForHelp.bind(this);
        this._mapRequest = this._mapRequest.bind(this);
    }

    async getHelpRequests() {
        const response = await fetch(API_URL + '/help-requests/', {
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                Authorization: `Bearer ${this.user.access_token}`
            },
        });

        if (response.status != 200) {
            console.error(response.status);
        }

        const data = await response.json();
        const requests: HelpRequest[] = [];
        if (data.data) {
            for (let request of data.data) {
                requests.push(this._mapRequest(request));
            }
        }
        return requests;
    }

    async getHelpRequest(requestID: string) {
        const response = await fetch(API_URL + `/help-requests/${requestID}`, {
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                Authorization: `Bearer ${this.user.access_token}`
            },
        });

        const data = await response.json();
        let helpRequest: HelpRequest;
        if (data.data) {
            const request = data.data;
            helpRequest = this._mapRequest(request);
            return helpRequest;
        }
    }

    async assignForHelp(helpRequestID: string) {
        const response = await fetch(API_URL + `/help-requests/${helpRequestID}`, {
            method: "PATCH",
            body: JSON.stringify({"accepted_by": "self"}),
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                Authorization: `Bearer ${this.user.access_token}`
            },
        });

        if (response.status != 200) {
            console.error(response);
        }
    }

    _mapRequest(request: any) {
        let helpRequest: HelpRequest;
        helpRequest = {
            id: request.id,
            full_name: request.full_name,
            products: request.products,
            created_at: new Date(Date.parse( request.created_at)),
            pickup_time: request.pickup_time,
            phone_number: request.phone_number,
            address: {
                address: request.address,
                longitude: request.longitude,
                latitude: request.latitude
            },
        };
        return helpRequest;
    }

}

export default HelpRequestsService;