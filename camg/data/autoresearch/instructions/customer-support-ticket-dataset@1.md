# OpenMLE-fast task

Task ID: `customer-support-ticket-dataset@1`

Native metric: `SupportTicketPriorityMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4054 bytes)
- `data/sample_submission.csv` (18824 bytes); columns: ["id", "Ticket Priority"]
- `data/test.csv` (617256 bytes); columns: ["id", "Customer Age", "Customer Gender", "Product Purchased", "Date of Purchase", "Ticket Type", "Ticket Channel", "Ticket Subject", "Ticket Description"]
- `data/train.csv` (2514553 bytes); columns: ["id", "Customer Age", "Customer Gender", "Product Purchased", "Date of Purchase", "Ticket Type", "Ticket Channel", "Ticket Subject", "Ticket Description", "Ticket Priority"]

## Public description

```
description.txt (51 lines)
sample_submission.csv (1695 lines)
test.csv (1695 lines)
train.csv (6776 lines)```

-> sample_submission.csv has 1694 rows and 2 columns.
Here is some information about the columns:
Ticket Priority (object) has 4 unique values: ['Medium', 'High', 'Critical', 'Low']
id (int64) has range: 9.00 - 8469.00, 0 nan values

-> test.csv has 1694 rows and 9 columns.
Here is some information about the columns:
Customer Age (int64) has range: 18.00 - 70.00, 0 nan values
Customer Gender (object) has 3 unique values: ['Other', 'Female', 'Male']
Date of Purchase (object) has 648 unique values. Some example values: ['2020-10-21', '2020-04-19', '2021-08-28', '2021-01-14']
Product Purchased (object) has 42 unique values. Some example values: ['GoPro Hero', 'Nest Thermostat', 'Nintendo Switch', 'Canon EOS']
Ticket Channel (object) has 4 unique values: ['Social media', 'Email', 'Chat', 'Phone']
Ticket Description (object) has 1692 unique values. Some example values: ["I'm having an issue with the Dyson Vacuum Cleaner. Please assist. I need assistance as soon as possible because it's affecting my work and productivity.", "I'm having an issue with the Amazon Echo. Please assist. I've already contacted customer support multiple times, but the issue remains unresolved.", "I'm having trouble connecting my Asus ROG to my home Wi-Fi network. It doesn't detect any networks, although other devices are connecting fine. What can be done to resolve this issue? I would like to see the I'm unable to find the option to perform the desired action in the Asus ROG. Could you please guide me through the steps?", "I'm having an issue with the GoPro Action Camera. Please assist. https://twitter.com/#!/Travolta (@TravoltaPla) The question that this post should Vinyl-loving kids want answered This problem started occurring after the recent software update. I haven't made any other changes to the device."]
Ticket Subject (object) has 16 unique values. Some example values: ['Software bug', 'Installation support', 'Payment issue', 'Network problem']
Ticket Type (object) has 5 unique values: ['Cancellation request', 'Refund request', 'Product inquiry', 'Technical issue', 'Billing inquiry']
id (int64) has range: 9.00 - 8469.00, 0 nan values

-> train.csv has 6775 rows and 10 columns.
Here is some information about the columns:
Customer Age (int64) has range: 18.00 - 70.00, 0 nan values
Customer Gender (object) has 3 unique values: ['Other', 'Female', 'Male']
Date of Purchase (object) has 730 unique values. Some example values: ['2021-07-04', '2021-11-21', '2021-08-16', '2021-03-27']
Product Purchased (object) has 42 unique values. Some example values: ['Canon EOS', 'Sony Xperia', 'LG Smart TV', 'Philips Hue Lights']
Ticket Channel (object) has 4 unique values: ['Social media', 'Chat', 'Email', 'Phone']
Ticket Description (object) has 6729 unique values. Some example values: ["I'm having an issue with the Microsoft Surface. Please assist. I've noticed a peculiar error message popping up on my Microsoft Surface screen. It says '{error_message}'. What does it mean?", "I'm having an issue with the Dell XPS. Please assist. The issue I'm facing is intermittent. Sometimes it works fine, but other times it acts up unexpectedly.", "I'm having an issue with the Bose SoundLink Speaker. Please assist. I'm unable to find the option to perform the desired action in the Bose SoundLink Speaker. Could you please guide me through the steps?", "I'm having an issue with the Dyson Vacuum Cleaner. Please assist. I've already contacted customer support multiple times, but the issue remains unresolved."]
Ticket Priority (object) has 4 unique values: ['Critical', 'Low', 'High', 'Medium']
Ticket Subject (object) has 16 unique values. Some example values: ['Refund request', 'Product compatibility', 'Software bug', 'Delivery problem']
Ticket Type (object) has 5 unique values: ['Technical issue', 'Billing inquiry', 'Cancellation request', 'Product inquiry', 'Refund request']
id (int64) has range: 1.00 - 8468.00, 0 nan values
