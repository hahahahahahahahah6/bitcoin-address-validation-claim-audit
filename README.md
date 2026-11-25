# Address claim audit

This offline static audit compares documented claims with Python source call patterns. It does not execute source code or make network requests.

Install and run:

```sh
python3 -m pip install bitcoin-address-validation-claim-audit
bitcoin-address-validation-claim-audit audit .
python3 -m bitcoin_address_validation_claim_audit audit . --json
```

Use `--fail-on medium` to include test-only evidence in the failure threshold; `--ignore PREFIX` may be repeated. The default threshold is high. Exit status is 0 for pass, 2 for findings at the threshold, and 1 for usage or I/O errors. `--verbose` adds the audited path.

The scanner reads root README and Markdown files beneath docs, excluding fenced blocks. Inline code counts. It normalizes case, contractions, hyphens and whitespace, and removes denial spans before looking for positive claims. It parses Python with the standard library, excludes symlinks and fixture, docs and example source, and treats tests separately. Syntax errors provide no evidence.

Recognized calls:

```
stdnum.bitcoin.validate
stdnum.bitcoin.is_valid
validators.btc_address
```

Generic named calls and resolved imports also count. Imports alone do not. Findings are:

```
documented-bitcoin-address-validation-claim-false
documented-no-bitcoin-address-validation-claim-false
```

A positive claim without production evidence is high severity, or medium if evidence occurs only in tests. A denial with production evidence is high severity.

## Differentiation

This audit does not cover generic input validation.
This audit does not cover ISBN book-number check digits.
This audit does not cover ISSN serial-number check digits.
This audit does not cover IBAN account-number check digits.
This audit does not cover UUID validation.
This audit does not cover semantic version validation.
This audit does not cover MAC address validation.
This audit does not cover BIC validation.
This audit does not cover cron expression validation.
This audit does not cover cron expression description.
This audit does not cover scheduled execution.
This audit does not cover calendar date validation.
This audit does not cover timeouts.
This audit does not cover card payment processing.
This audit does not cover card detail extraction.
This audit does not cover one-time-code or link authentication.
This audit does not cover password authentication.
This audit does not cover password hashing.
This audit does not cover password generation.
This audit does not cover PDF encryption.
This audit does not cover email sending.
This audit does not cover SMS sending.
This audit does not cover document extraction.
This audit does not cover barcode decoding.
This audit does not cover email validation.
This audit does not cover phone number validation.
This audit does not cover password strength.
This audit does not cover JSON Schema validation.
This audit does not cover credit card validation.
This audit does not cover domain name validation.
This audit does not cover URL validation.
This audit does not cover IP address validation.
This audit does not cover JSON decoding.
This audit does not cover regular expression matching.
This audit does not cover URL parsing.
This audit does not cover network fetching of web addresses.
This audit does not cover DNS resolution.
This audit does not cover barcode generation for account numbers.
This audit does not cover account number extraction.
This audit does not cover vehicle number extraction.
This audit does not cover vehicle number decoding or make, model and year lookup.
This audit does not cover vehicle history lookup.
This audit does not cover hex color validation.
This audit does not cover ORCID validation.
This audit does not cover ISNI validation.
This audit does not cover DOI validation and resolution.
This audit does not cover CUSIP validation.
This audit does not cover SEDOL validation.
This audit does not cover ISIN validation.
This audit does not cover security record lookup.
This audit does not cover securities identifier extraction.
This audit does not cover IMEI validation.
This audit does not cover MEID validation.
This audit does not cover ESN validation.
This audit does not cover ISMN validation.
This audit does not cover ISAN validation.
This audit does not cover GRid validation.
This audit does not cover EAN validation.
This audit does not cover generic serial number validation.
This audit does not cover FIGI validation.
This audit does not cover financial instrument record lookup.
This audit does not cover financial instrument identifier extraction.
This audit does not cover ISRC validation.
This audit does not cover Ethereum address validation.
This audit does not cover Binance Smart Chain address validation.
This audit does not cover Tron address validation.
This audit does not cover Litecoin address validation.
This audit does not cover Dogecoin address validation.
This audit does not cover transaction hash validation.
This audit does not cover private key or Wallet Import Format key validation.
This audit does not cover block explorer balance or transaction lookup.
This audit does not cover address generation.
This audit does not cover address extraction.
This audit does not cover payment receipt confirmation.
This audit does not cover spreadsheet reading.
This audit does not cover spreadsheet generation.
This audit does not cover word-document reading.
This audit does not cover word-document generation.
This audit does not cover presentation reading.
This audit does not cover presentation generation.
This audit does not cover PDF extraction.
This audit does not cover PDF generation.
This audit does not cover PDF merging.
This audit does not cover PDF splitting.
This audit does not cover PDF rotation.
This audit does not cover PDF form-filling.
This audit does not cover PDF watermarking.
This audit does not cover PDF redaction.
This audit does not cover PDF compression.
This audit does not cover PDF annotation.
This audit does not cover table extraction.
This audit does not cover OCR.
This audit does not cover document extraction claims.
This audit does not cover e-signatures.
This audit does not cover screen recording.
This audit does not cover video generation.
This audit does not cover QR code generation.
This audit does not cover barcode generation claims.
This audit does not cover barcode scanning.
This audit does not cover audio mixing.
This audit does not cover audio generation.
This audit does not cover audio editing.
This audit does not cover source separation.
This audit does not cover speech recognition.
This audit does not cover text-to-speech.
This audit does not cover noise suppression.
This audit does not cover music generation.
This audit does not cover music transcription.

## Limitations

Static matching cannot establish behavior; dead code counts.
Aliases beyond the tracked imports may be missed.
Only exact listed wording is recognized.
Denial handling depends on the listed denial wording.
Each evidence route must occur in one module.
The stdnum route rejects testnet addresses.
The stdnum route rejects taproot addresses.
The stdnum route accepts mixed-case bech32 strings.
The stdnum route accepts upper-case bech32 strings.
The stdnum route rejects lowercase legacy examples because base58 is case-sensitive.
The validators route checks bech32 by pattern and can accept a bad checksum.
The validators route accepts testnet by pattern.
The validators route accepts taproot by pattern.
Neither library establishes on-chain existence.
Neither library establishes an account balance.
Both libraries reject the invalid legacy example in the validators documentation.
A compact call only reformats.
A b58decode call only decodes and checks the alphabet.
A b32decode call handles five-bit values.
A bech32_checksum call computes an integer.
Ethereum validator calls concern another chain.
Binance Smart Chain validator calls concern another chain.
Tron validator calls concern another chain.
A regular expression alone does not count.
A length check alone does not count.
A prefix check alone does not count.
An alphabet membership check alone does not count.
Address lookup alone does not count.
Address generation alone does not count.
Transaction validation alone does not count.
Payment validation alone does not count.
Block validation alone does not count.
Private key validation alone does not count.
Wallet Import Format key validation alone does not count.
Litecoin address calls alone do not count.
Dogecoin address calls alone do not count.
External process invocations do not count.
A bare import, string, filename, extension, comment, or name reference is not evidence.
A roadmap, changelog or todo in scanned prose still counts as a claim.
A document outside the root readme and docs directories is not scanned.
A local definition shadows the corresponding route name.

```
validate bitcoin address
```
The wording above can refer to a manual runbook step; review its context.

```
bitcoin address validation
```
The wording above can refer to a roadmap item; review its context.

```
bitcoin address validator
```
The wording above can refer to a hosted page; review its context.

```
bitcoin address check
```
The wording above can refer to a field-presence lint rule; review its context.

```
check bitcoin address
```
The wording above can refer to a manual runbook step; review its context.

```
verify bitcoin address
```
The wording above can refer to a visual wallet-ownership confirmation; review its context.

```
bitcoin address verification
```
The wording above can refer to an external service result; review its context.

```
validate btc address
```
The wording above can refer to a manual runbook step; review its context.

```
btc address validation
```
The wording above can refer to a specification section; review its context.

```
valid bitcoin address
```
The wording above can refer to example output; review its context.

```
bitcoin address is valid
```
The wording above can refer to example output; review its context.

```
bitcoin address is invalid
```
The wording above can refer to example error text; review its context.

```
bitcoin address validity
```
The wording above can refer to a configuration flag or column; review its context.

```
bitcoin address format validation
```
The wording above can refer to a format description; review its context.

```
validate bitcoin wallet address
```
The wording above can refer to a manual runbook step; review its context.

```
bitcoin wallet address validation
```
The wording above can refer to a specification section; review its context.

```
btc address check
```
The wording above can refer to a wallet setup checklist; review its context.

```
check btc address
```
The wording above can refer to a manual runbook step; review its context.

```
verify btc address
```
The wording above can refer to a visual wallet-ownership confirmation; review its context.

```
validate bitcoin address format
```
The wording above can refer to a format description; review its context.

```
bitcoin
```
The wording above can refer to the currency alone; review its context.

```
bitcoin address
```
The wording above can refer to an address alone; review its context.

```
validate bitcoin
```
The wording above can refer to a transaction, payment or block; review its context.

```
btc
```
The wording above can refer to the ticker alone; review its context.

```
wallet address
```
The wording above can refer to an address on any chain; review its context.

```
check digit
```
The wording above can refer to a checksum alone; review its context.

```
address
```
The wording above can refer to an address alone; review its context.

```
blockchain address
```
The wording above can refer to an address on any chain; review its context.
