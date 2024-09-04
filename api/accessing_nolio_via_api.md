## Accessing Nolio API with Insomnia

### Prerequisites

- Install [Insomnia](https://insomnia.rest/download).
- Obtain API credentials and root certificate.

### Setup

1. **Import Project:**
    - In Insomnia, go to `Preferences` > `Data` > `Import Data` > `From File`.
    - Load the `project.json` file.
2. **Configure Environment:**
    - Add `base_url`, `username`, and `password` in environment settings.
3. **Add Certificates:**
    - In `Preferences` > `Certificates`, click `Add Certificate`.
    - Upload the root certificate for `base_url`.

### Authentication

- Set Basic Auth for requests using `username` and `password`.

### Making Requests

- Use existing or new requests configured with Basic Auth.

### API Documentation

- Check the [Official Nolio Documentation](https://www.notion.so/Nolio-api-3171a9fb5ee448f6ad54cdb2e4702524?pvs=21) for API endpoints.
