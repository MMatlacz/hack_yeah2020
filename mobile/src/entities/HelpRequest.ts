interface HelpRequest {
    id: string,
    full_name: string,
    created_at: Date,
    pickup_time: string,
    phone_number: string,
    products: [string],
    address: {
        "address": string
        "longitude": number,
        "latitude": number,
    }
}