# 1. Warming up with two support tickets:

## Ticket #1

Hello,

Thanks for sending us this over and sure we can help.
After looking into your map html file I noticed the problem lays in `function openPopup` where you correctly created the html for the popup in the variable named `content`. However, you did not add the html to the `popup` variable.

I have attached a html file named `fixed_map.html` with the addition on line 72 that adds the html to the popup variable via the `popup.setContent()` function. 

Let me know if this works for you.

Best,

Gabriel

## Ticket #2

Hello,

Thanks for sending this over and sure we can help.

Let us break it down in sections

### Section 1
```sql
    FROM european_countries e
    JOIN populated_places p
    ON ST_Intersects(p.the_geom, e.the_geom)
```
Starting at `FROM`, this is referring to a table called `european_countries` which is renamed as `e` and this is the main table we are going to be querying.
The `JOIN` refers to joining the `european_countries` table mentioned above with another table called `populated_places` which is renamed as `p`.

We are joining these tables using a `ST_Intersects`, which is a spatial join. It joins rows if it's lat and lons intersects or touches with another table's lat and lon on each row.

In this case `ST_Intersects` is joining rows in the `european_countries` table on the `the_geom` column if they intersect with any row in the `populated_places` table on `the_geom` column. Meaning each matching `populated_places` row will be added to each matching row in the `european_countries` table.  

*Keep in mind if there are multiple matches for `ST_Intersects` then the rows in `european_countries` will be duplicated so the matched row in `populated_places` table can be added to the new joined table.*


### Section 2

```sql
      SELECT e.name,
             count(*) AS counts,
             sum(p.population) as population
``` 

Then in this section we are filtering for specific data from the joined table we created above to create an output table.

The output table will only have three columns:

* `e.name`: We are getting all the names from the `name` column of `european_countries` section of the joined table we created above.
* `counts`: We are creating this column via the `AS counts` section. This column is counting the total instances of each name found in the new joined table.
* `population`: We are creating this column via the `AS sum` section again. This column is adding up all rows in the populations for each `e.name`. *Remember there could be multiple populations for `e.name` because of the join*


### Section 3

```sql
    GROUP BY e.name
``` 
Finally we are ordering this new created and filtered table mentioned in section 2 & 3 by the column `name` from specifically the `european_countries` table part of the joined table.

Hope this was hopeful,

Gabriel
