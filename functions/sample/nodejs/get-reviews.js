const express = require('express');
const app = express();
const port = process.env.PORT || 3002;
const Cloudant = require('@cloudant/cloudant');

// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: 'b51Dl8VJYn_i7aHxRU75BDsUaKQuhpk5Sz-a4CAlgPcf' } }, // Replace with your IAM API key
            url: 'https://86357358-812b-4fdd-9d5e-41711a23ed3d-bluemix.cloudantnosqldb.appdomain.cloud', // Replace with your Cloudant URL
        });

        const db = cloudant.use('reviews');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

// Define a route to get all reviews with optional state and ID filters
app.get('/reviews/get', (req, res) => {
    const { state, id, dealership } = req.query;
    console.log(req.query)
    // Create a selector object based on query parameters
    const selector = {};
    if (state) {
        selector.state = state;
    }
    
    if (id) {
        selector.id = parseInt(id); // Filter by "id" with a value of 1
    }
    if(dealership) {
        selector.dealership = parseInt(dealership)
    }

    const queryOptions = {
        selector,
        limit: 10, // Limit the number of documents returned to 10
    };

    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching dealer reviews:', err);
            res.status(500).json({ error: 'An error occurred while fetching reviews.' });
        } else {
            console.log(body)
            const reviews = body.docs;
            res.json(reviews);
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});