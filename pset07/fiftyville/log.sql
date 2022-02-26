-- Keep a log of any SQL queries you execute as you solve the mystery.
-- View all crime scenes on July 28, 2021
SELECT
    *
FROM
    crime_scene_reports csr
WHERE
    csr."year" = 2021
    AND csr."month" = 7
    AND csr."day" = 28;

/* Returns interviews of the witnesses */
SELECT
    i.name,
    i.transcript
FROM
    interviews i
WHERE
    i."year" = 2021
    AND i."month" = 7
    AND i."day" = 28
ORDER BY
    i."name";

/* Returns all passengers left fiftyville one day after the crime */
SELECT
    *
FROM
    passengers pa
    LEFT JOIN people pe ON pa.passport_number = pe.passport_number
WHERE
    pa.flight_id IN(
        SELECT
            f.id
        FROM
            flights f
        WHERE
            f.origin_airport_id = 8
            AND f."year" = 2021
            AND f."month" = 7
            AND f."day" = 29
    );

/* Returns cars that left the bakery shop after the crime */
SELECT
    *
FROM
    bakery_security_logs bsl
WHERE
    bsl."year" = 2021
    AND bsl."month" = 7
    AND bsl."day" = 28
    AND bsl."hour" = 10
    AND bsl."minute" >= 15
    AND bsl."minute" <= 25
    AND bsl.activity = 'exit'
ORDER BY
    bsl."minute";

/* Returns personal ID of suspects who withdrawing money at Leggett Street on 
 the same day */
SELECT
    ba.person_id
FROM
    atm_transactions atm
    LEFT JOIN bank_accounts ba ON atm.account_number = ba.account_number
    LEFT JOIN people pe ON pe.id = ba.person_id
WHERE
    atm.atm_location = 'Leggett Street'
    AND atm."year" = 2021
    AND atm."month" = 7
    AND atm."day" = 28;

/* Returns calls that less than 1 min made on the same day */
SELECT
    pe.id
FROM
    phone_calls pc
    LEFT JOIN people pe ON pe.phone_number = pc.caller
WHERE
    pc.duration < 60
    AND pc."year" = 2021
    AND pc."month" = 7
    AND pc."day" = 28;

/* The THIEF */
SELECT
	*
FROM
	passengers pa
	LEFT JOIN people pe ON pa.passport_number = pe.passport_number
WHERE
	-- the thief took the earliest flight on the next day after the crime
	pa.flight_id IN(
		SELECT
			f.id FROM flights f
		WHERE
			f.origin_airport_id = 8
			AND f. "year" = 2021
			AND f. "month" = 7
			AND f. "day" = 29
		ORDER BY
			f. "hour", f. "minute"
		LIMIT 1)
	-- the thief left the bakery shop within 10 mins
	AND pe.license_plate IN(
		SELECT
			bsl.license_plate FROM bakery_security_logs bsl
		WHERE
			bsl. "year" = 2021
			AND bsl. "month" = 7
			AND bsl. "day" = 28
			AND bsl. "hour" = 10
			AND bsl. "minute" >= 15
			AND bsl. "minute" <= 25
			AND bsl.activity = 'exit'
		ORDER BY
			bsl. "minute")
	-- the theif withdrawned money at Leggett Street on the same day
	AND pe.id IN(
		SELECT
			ba.person_id FROM atm_transactions atm
		LEFT JOIN bank_accounts ba ON atm.account_number = ba.account_number
		LEFT JOIN people pe ON pe.id = ba.person_id
	WHERE
		atm.atm_location = 'Leggett Street'
		AND atm. "year" = 2021
		AND atm. "month" = 7
		AND atm. "day" = 28)
	-- the theft made a call that less than a minute when leaving the scene
	AND pe.id in(
		SELECT
			pe.id FROM phone_calls pc
		LEFT JOIN people pe ON pe.phone_number = pc.caller
	WHERE
		pc.duration < 60
		AND pc. "year" = 2021
		AND pc. "month" = 7
		AND pc. "day" = 28);

/* The city the thief ESCAPED TO */
SELECT
	ai.city
FROM
	passengers pa
	LEFT JOIN people pe ON pa.passport_number = pe.passport_number
	LEFT JOIN flights f ON f.id = pa.flight_id
	LEFT JOIN airports ai ON ai.id = f.destination_airport_id
WHERE
	pa.flight_id IN(
		SELECT
			f.id FROM flights f
		WHERE
			f.origin_airport_id = 8
			AND f. "year" = 2021
			AND f. "month" = 7
			AND f. "day" = 29
			AND pe. "name" = 'Bruce');

/* The ACCOMPLICE */
SELECT
    pe2."name"
FROM
    phone_calls pc
    LEFT JOIN people pe1 ON pe1.phone_number = pc.caller
    LEFT JOIN people pe2 ON pe2.phone_number = pc.receiver
WHERE
    pc.duration < 60
    AND pc."year" = 2021
    AND pc."month" = 7
    AND pc."day" = 28
    AND pe1."name" = 'Bruce'