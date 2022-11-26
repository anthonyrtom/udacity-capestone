#!/bin/bash
export DATABASE_URL='postgresql://postgres:pass123@localhost:5432/taxentitydb'
export AUTH0_DOMAIN='antony-tax-entity.us.auth0.com'
export API_AUDIENCE='TaxEntity'
export FLASK_APP=app
export accountant_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNEYXlHMUJmeFhRQ0ZuVjlmWG0wbCJ9.eyJpc3MiOiJodHRwczovL2FudG9ueS10YXgtZW50aXR5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzYwMzFlOTBiZDRmNGFmMDI3NDhhYTQiLCJhdWQiOiJUYXhFbnRpdHkiLCJpYXQiOjE2Njk0NjI4MDIsImV4cCI6MTY2OTU0OTIwMiwiYXpwIjoiajFCVWNWZlNyTEdmSVVZRkdIczNUOEM1WEtSemVaRGUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY2NvdW50YW50cyIsInBhdGNoOmFjY291bnRhbnRzIiwicG9zdDphY2NvdW50YW50cyJdfQ.c_UA9BjCbjC-Oe8GK8nda0juRLTFwEiqQolNMMQkLSBIYeKUB4fTHLShlV-d49fWxrGisMoN_jGrmzkZ3yKO7cDbdeEWGs7kmop1BAfIX2HgPplmfkvuUEcGkEwVmn-LPPabymYOsyPtZsUt7KZk1KMDRh_6pL-BMgbvnELcqSuYffEnhED4MBcwU4KJGxI01RklJBcLXbu4sHiampOSIJGq5Ncx2DzQCwwOFVGkYD_Isd_ZqAeaF2s8JARCfaemGHf9AubcgjipR6KT4nbEEjvAuV_HauHrKu-Cl49k1aVMWIaULBJGDdxe2Ib9q4_r7wd0KF_qm61rtjI8U-D9CA'
export taxentity_token='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlNEYXlHMUJmeFhRQ0ZuVjlmWG0wbCJ9.eyJpc3MiOiJodHRwczovL2FudG9ueS10YXgtZW50aXR5LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MzYwMzIzZDdmYjYzZjViOGFmNzkwZGMiLCJhdWQiOiJUYXhFbnRpdHkiLCJpYXQiOjE2Njk0NjI5NjgsImV4cCI6MTY2OTU0OTM2OCwiYXpwIjoiajFCVWNWZlNyTEdmSVVZRkdIczNUOEM1WEtSemVaRGUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTp0YXhlbnRpdGllcyIsImdldDp0YXhlbnRpdGllcyIsInBhdGNoOnRheGVudGl0aWVzIiwicG9zdDp0YXhlbnRpdGllcyJdfQ.Upel6b2EXLjHT3X8rcK-rajaZuer2GNvLf_bTYhnUNVyNZaAqTHh9MNJWHnvG_xtRB87OBuJ9dN4Tqyd0363gR8XJRawIaaTyYN2kuHkPbfZdbc295VZ5D3wZBXQI68nWDpKmPHpQpz-KVwgocMqp8kzfKJxS20-dreTANo60DHtsnhzFT3zo9JKkpvx_mRPy0UcWZ-gRLFtTlS1Ei6m3oE4fFUl1dXKAJiNtW0SrjvqOJmoVOBqbSsPC3JDPQlrxIvLh8QeWwSQ1rrct5zCzVk8q5U8qQg5zBvDzd3pxSKr0tUZ4o8k5T-WSGGT9d2lowAVjjN6FN7YtRp5gZsBFg'