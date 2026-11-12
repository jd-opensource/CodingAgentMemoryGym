# OpenMLE-fast task

Task ID: `womens-ecommerce-clothing-reviews@1`

Native metric: `WomensEcommerceReviewMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (4767 bytes)
- `data/sample_submission.csv` (42299 bytes); columns: ["review_id", "Rating"]
- `data/test.csv` (1671185 bytes); columns: ["review_id", "Clothing ID", "Age", "Title", "Review Text", "Division Name", "Department Name", "Class Name"]
- `data/train.csv` (6742003 bytes); columns: ["review_id", "Clothing ID", "Age", "Title", "Review Text", "Division Name", "Department Name", "Class Name", "Rating"]

## Public description

```
description.txt (44 lines)
sample_submission.csv (4699 lines)
test.csv (5673 lines)
train.csv (22556 lines)```

-> sample_submission.csv has 4698 rows and 2 columns.
Here is some information about the columns:
Rating (int64) has 1 unique values: [5]
review_id (int64) has range: 100000.00 - 123483.00, 0 nan values

-> test.csv has 4698 rows and 8 columns.
Here is some information about the columns:
Age (int64) has range: 19.00 - 94.00, 0 nan values
Class Name (object) has 19 unique values. Some example values: ['Dresses', 'Knits', 'Blouses', 'Sweaters']
Clothing ID (int64) has range: 3.00 - 1203.00, 0 nan values
Department Name (object) has 6 unique values: ['Bottoms', 'Dresses', 'Tops', 'Intimate', 'Jackets', 'Trend', nan]
Division Name (object) has 3 unique values: ['General', 'General Petite', 'Initmates', nan]
Review Text (object) has 4515 unique values. Some example values: ["I didn't realize that the grey sleeves are attached (i assumed that was just an undershirt on the model). needless to say it looks cheap and poorly made. will be returning", 'I love this jump suit.. sorta. looks great on but the dye rubs off on your skin. i washed it and its still happening. when you put your hand in your pockets, they come out blue, knees are blue, thighs, etc. i looked dirty by the end of the day. wish i could return it. fit and look great... not great after wear.', 'I tried this on in my usual xs (5\'5", 128lbs) and it fit like a dream. i was instantly in love. until i looked from the side and realized it was cut up way too short. i have a longer torso and shorter legs and this came up past my finger tips if i stood with my arms down. no way could i wear this as a dress. as a tunic definitely though, but i was really hoping to find a nice, versatile fall dress. it was a let down but i still may consider purchasing it because the material was so soft and it f', "I usually wear a 2-4 in retailer dresses and i was surprised the xs fit better than the s. very pretty, really perfect color for fall. i like that it's not tight or constricting so you can wear it for every day and not feel like it's difficult to move around. the longer length is nice too for. bonus that it's not dry clean only. my only problem with this dress is it's all polyester, which is just cheap fabric. if it wasn't for that, i'd give it 5 stars."]
Title (object) has 3200 unique values. Some example values: ['Love it!', 'Beautiful', 'Great dress', 'Love!']
review_id (int64) has range: 100000.00 - 123483.00, 0 nan values

-> train.csv has 18788 rows and 9 columns.
Here is some information about the columns:
Age (int64) has range: 18.00 - 99.00, 0 nan values
Class Name (object) has 19 unique values. Some example values: ['Dresses', 'Knits', 'Blouses', 'Sweaters']
Clothing ID (int64) has range: 0.00 - 1205.00, 0 nan values
Department Name (object) has 6 unique values: ['Jackets', 'Dresses', 'Intimate', 'Tops', 'Bottoms', nan, 'Trend']
Division Name (object) has 3 unique values: ['General', 'Initmates', 'General Petite', nan]
Rating (int64) has 5 unique values: [1, 5, 4, 3, 2]
Review Text (object) has 18120 unique values. Some example values: ["Perfect fit and i've gotten so many compliments. i buy all my suits from here now!", 'I purchased this and another eva franco dress during retailer\'s recent 20% off sale. i was looking for dresses that were work appropriate, but that would also transition well to happy hour or date night. they both seemed to be just what i was looking for. i ordered a 4 regular and a 6 regular, as i am usually in between sizes. the 4 was definitely too small. the 6 fit, technically, but was very ill fitting. not only is the dress itself short, but it is very short-waisted. i am only 5\'3", but it fe', "I bought this shirt at the store and after going home and trying it on, i promptly went online and ordered two more! i've gotten multiple compliments anytime i wear any of them. great for looking put together with no fuss. \r\npeople that have commented there's were destroyed in the wash didn't read the care label which says dry clean.", "Lightweight, soft cotton top and shorts. i think it's meant to be a beach cover-up but i'm wearing it as a thin, light-weight summer outfit on these hot hot days. the top has a loose elastic around the bottom which i didn't realize when i ordered it, but i like it and it matches the look in the photos. and the shorts are very low-cut - don't expect them up around your waist. again, i like that. some might want to wear a cami underneath because it's a thin cotton but i'm fine as-is. i bought it i"]
Title (object) has 11499 unique values. Some example values: ['Love it!', 'Love', 'Beautiful', 'Love!']
review_id (int64) has range: 100003.00 - 123485.00, 0 nan values
