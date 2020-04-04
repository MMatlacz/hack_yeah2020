import { API_URL } from 'react-native-dotenv'


class HelpRequestsService {
    api_url: string;
    user: object;

    constructor(user: object) {
        this.user = user;
        this.api_url = API_URL;

        this.getHelpRequests = this.getHelpRequests.bind(this);
        this.assignForHelp = this.assignForHelp.bind(this);
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
                requests.push({
                    id: request.id,
                    full_name: request.full_name,
                    products: request.products,
                    created_at: new Date(Date.parse( request.created_at)),
                    address: {
                        address: request.address,
                        longitude: request.longitude,
                        latitude: request.latitude
                    },
                });
            }
        }
        return requests;
    }

    async assignForHelp(helpRequestID: string) {
        const response = await fetch(API_URL + `/help-requests/${helpRequestID}`, {
            method: "PATCH",
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                Authorization: `Bearer ${this.user.access_token}`
            },
        });
    }

}

export default HelpRequestsService;