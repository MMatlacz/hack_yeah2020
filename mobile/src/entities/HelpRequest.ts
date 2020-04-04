interface HelpRequest {
    id: string,
    full_name: string,
    created_at: Date,
    products: [string],
    address: {
        "address": string
        "longitude": number,
        "latitude": number,
    }
}