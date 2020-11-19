JSON should be streamed instead of leaded to avoid memory overflow
[source](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1555762)

You can use the provided `Id` field as the Mongo `_id` field, but it is unclear if that will be suitable or not.
[source](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1557054)

The C function `ispunct` is recommended to determine if a character can be considered punctuation or not, so it seems that anything that is not whitespace or alphanumeric can be considered punctuation.
[source](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1557054)

The user ID report should give the number of votes received (not given). All vote types are considered.\
`VoteTypeId` can be mostly ignored in this assignment. Its intended purpose would be to distinguish between different vote types in a real system (upvotes vs downvotes for example).
[source 1](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1558404), [source 2](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1561907)

Unlike the previous project, no logout functionality is needed.
[source](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1558228)

Phase 1 should complete in 5 minutes in the **demo**. The demo files are around 5 times as big as the sample files.
[source](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1559667)

The score field in Posts is the total number of votes of type 2 on the post.
[source](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1561907)

Extracted terms can be treated as a set since duplicates don't add any value to the index.
[source](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1564667)

Users can create new tags. If an existing tag is specified, its count should be updated, if a new tag is specified, it should be added to the Tags collection.
[source](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1564987)
