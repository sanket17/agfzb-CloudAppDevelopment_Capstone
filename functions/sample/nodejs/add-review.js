const express = require('express');
const app = express();
const port = process.env.PORT || 3004;
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
app.post('/reviews/post', (req, res) => {
    review = {}
    review["time"] = req.body.time
    review["dealership"] = req.body.dealership
    review["review"] = req.body.review
    review["purchase"] = req.body.purchase
    review["purchase_date"] = req.body.purchase_date
    review["name"] = req.body.name
    review["car_make"] = req.body.car_make
    review["car_model"] = req.body.car_model
    review["car_year"] = req.body.car_year
    console.log(review, req.body)
    db.insert(review, (err, body) => {
        if (err) {
            console.error('Error creating dealer review:', err);
            res.status(500).json({ error: 'An error occurred while creating review.' });
        } else {
            return body.ok
        }
    });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});