# data-job-crawler

# Testing

## Manual Tests

- [ ] Run the spiders (eg. WttjLinksSpider + WttjSpider)
- With the output txt file 
  - [ ] Search for links in the first, last and middle pages of results.
  - [ ] Compare number of links with `item_scraped_count` from 2nd spider
- [ ] Check logs for errors' tracebacks

## End-to-end test

The input data, a job's web page, has to end up in raw_jobs with the intended fields.
- Copy a URL and query `raw_jobs` 

```
SELECT url, title, company, location, type, industry, remote, created_at FROM raw_jobs WHERE url LIKE 'https://www.welcometothejungle.com/fr/companies/foxintelligence/jobs/senior-data-analyst-team-quality_paris%';
```

```
SELECT text FROM raw_jobs WHERE url LIKE 'https://www.welcometothejungle.com/fr/companies/foxintelligence/jobs/senior-data-analyst-team-quality_paris%';
```
