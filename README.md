# Hello
## TL;DR
Please find my submission here. My test lives in `QA-Automation/tests.py`. From root run `pytest -v QA-Automation/tests.py` headlessly, or `pytest -v QA-Automation/tests.py --headed` if you wanna see what's going on.
## Test architecture
In the original readme, under [Test Coverage Expectations](https://github.com/CydarLtd/qa-automation-interview?tab=readme-ov-file#test-coverage-expectations), 4 bullet points were listed. This makes me think you were expecting at least 4 separate tests. However, I created only one test, which covers all of those areas (and some more). Let's now argue about why I did it this way *(I know I'm about to argue with myself, but I will imagine the counterpoints)*

| Question | Arguments |
|----------|-----------|
|*"Would the tests not be more maintainable if they were separated?"*|**Not really. All common, reusable testing functionality is abstracted into helper functions that actually do the lifting. Most updates and modifications would be limited to these functions**|
|*"But if the test fails early on, will we not lose the coverage later down the test that would have been carried out if they were separated?"*|**It depends. If there is leftover data from failed tests that were unexpected in the upcoming ones (e.g. leftover todos that were not deleted), then all subsequent tests will also fail. If all tests are sanitised prior to running in a before hook, and this one is split into 4 individual (very short) ones, a lot of time is lost, which means lost productivity, more time spent in CI, and more money spent.**|
|*"Shouldn't each test be responsible for testing one area of the app for readability?"*|**Define 'one area'. I believe a test should cover a key workflow (with additional coverage related to the workflow). This one mainly focuses on creation and deletion. In addition, it also covers data partitioning. As mentioned before, I could have created a separate test just for the partition, but that would involve creating data as user 1 (to ensure user  2 cannot see it), which would be repeating coverage, therefore, wasting time and money in the long run.**|

## Test coverage
### Overview
Firstly, I want to mention the bonus point "Measure Test Coverage". This would be a trivial, yet counterproductive task. The aim should never be **X% test coverage**, since what we're testing is a lot more important than how much we are testing. E.g. aiming for (let's say) 90% test coverage would be a waste of time and resources, if only 40% of the app functionality is critical for user experience. 

Essentially, what I mean is we should only test parts of the app, that if they break in the middle of the night, someone is getting woken up to fix them: **CRITICAL COMPONENTS**. A good example (what I encountered and mentioned later in this readme) is adding tasks with invalid titles. If a user encountered an issue where they can add a task with an empty title:

- They can delete it they you want
- They can ignore it they you want

If we see it, we should probably fix it, but spending test coverage on this would be wasteful. You could argue that "it might break something in the backend", but it probably won't, since they have their own test cases and validation to handle something like this, where it is important, not in an end-to-end test.
### Actual coverage

**Required in the test outlines**
- [x] Login with valid credentials
- [x] Redirect to dashboard after login
- [x] Logout functionality
- [x] Adding a new task
- [x] Verifying the task appears in the list
- [x] Completing a task
- [x] Deleting a task
- [x] User A cannot see tasks of user B
- [x] User B cannot see tasks of user A
- [x] Verifying more than 5 tasks
- [x] Verifying no tasks are skipped or duplicated (does not verify that only 5 tasks are displayed per page, but see my argument above for this)

**Other test functionality I added for good coverage of these workflows**
- [x] Before hook that can be used before each test to set up the test environment
  - Login, redirect validation, data deletion, etc.
- [x] Login attempt with invalid credentials (not actually used in this test, but the function has the option to expect bad creds)
- [x] Test detail verification
  - Title
  - Creating user
  - Timestamp of creation (note: additional checks are required here, but I already spent too much time -- see comment)
- [x] Checking for toast notification
  - These are used to check that a test step has finished completing (imagine it takes some time for the task to be deleted, but the test runs on and fails because the site is not in an expected state)
  - These checks ensure that the given task has been successfully deleted and it is safe to move on (instead of hardcoding waits)
     
**Coverage I wanted to add, but I already spent too much time on this**
- [ ] Attempting to log in with bogus creds
- [ ] Once logged in, the correct user is logged not (not somehow a different user)

## Best practices
I'm getting carried away, and you are probably falling asleep, so I'll make this a turbo round. 

**Done:**
- [x] Common functionality abstracted into helper functions
- [x] Selectors using `data-testid` not some role or class
  - These can change at any time during development, so these are not reliable and would make tests potentially flaky
  - I added these testids to the elements
- [x] Asserting functionality to check the page is in an expected state
  - I.e. if stuff took some time to happen, these checks will ensure stuff already happened instead of hard-coded waits
- [x] Functions that aren't obvious have detailed comments on why and how they do things
- [x] Before hook cleans up previous tests
- [x] Checks that crucial UI components are visible (not hidden under some other element)

**Stuff I want to do, but again I spent too much time already**
- [ ] Create a function to find a task by name (commonly used -- currently this is 2 lines of code, when it could be one)
- [ ] Extra validation of the description (see comments)
- [ ] Extract creds into protected `.env` file
- [ ] Other helper functions that are common to help readability (like checking for a toast notification)
- [ ] Probably others I forget, I always have crazy ideas to improve stuff

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
