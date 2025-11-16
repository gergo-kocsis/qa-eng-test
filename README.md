# Hello
## TL;DR
Please find my submission here. My test lives in `QA-Automation/tests.py`. From root run `pytest -v QA-Automation/tests.py` headlessly, or `pytest -v QA-Automation/tests.py --headed` if you wanna see what's going on.
## Test architecture
In the original readme, under [Test Coverage Expectations](https://github.com/CydarLtd/qa-automation-interview?tab=readme-ov-file#test-coverage-expectations), 4 bullet points were listed. This makes me think you were expecting at least 4 separate tests. However, I created only one test, which covers all of those areas (and some more). Let's now argue about why I did it this way *(I know I'm about to argue with myself, but I will imagine the counterpoints)*

| Question | Arguments |
|----------|-----------|
|*"Would the tests not be more maintainable if they were separated?"*|**Not really. All common, reusable testing functionality is abstracted into helper functions that actually do the lifting. Most updates and modifications would be limited to these functions**|
|*"But if the test fails early on, will we not lose the coverage later down the test that would have been carried out if they were separated?"*|**It depends. If there is leftover data from failed tests that were unexpected in the upcoming ones (e.g. leftover todos that were not deleted), then all subsequent tests will also fail. If all tests are sanitised prior to running in a before hook and this one is split into 4 individual (very short) ones, a lot of time is lost, which means lost productivity, more time spent in CI, more money spent.**|
|*"Shouldn't each test be responsible for testing one area of the app for readability?"*|**Define 'one area'. I believe a test should cover a key workflow (with additional coverage related to the workflow). This one mainly focuses on creation and deletion. In addition, it also covers data partitioning. As mentioned before, I could have created a separate test just for the parition, but that would involve creating data as user 1 (to ensure user  2 cannot see it), which would be repeating coverage, therefore, wasting time and money in the long run.**|

## Test coverage

## Bugs found & fixed
I should mention I didn't spend much time manually QAing the software, mostly just focused on areas that were broken for the automation. I could have spent more time manually trying to break this app, but I didn't want to spend much more time on this test than recommended.
### 1) Any page that was not 0 showed the contents of page n + 1
```
- start = (page + 1) * ITEMS_PER_PAGE 
+ start = (page) * ITEMS_PER_PAGE
```
### 2) All todos were displayed -- created by any user, not just the current user
```
- tasks = Task.objects.all()
+ tasks = Task.objects.filter(user=request.user)
```
### 3) Perhaps not a bug, but if the task title was invalid, there was no error message
*Also as mentioned in the code, the `messages.error` has no formatting, like the other message options, and just looks bland (I didn't spend time on making this nicer)*
```
if title:
    Task.objects.create(user=request.user, title=title)
    messages.success(request, 'Task added successfully!')

+ # ADDITION: There was no error message for this - also no css for error
+ else:
+     messages.error(request, 'Task title is invalid!')
return redirect('dashboard')
```
