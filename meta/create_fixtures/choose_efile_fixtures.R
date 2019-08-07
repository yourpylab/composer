library(tidyverse)

all_efiles <- read_csv("/dmz/github/analysis/composer/tmp/efile_indices/all_efiles.csv", col_types=c(.default="c"))

amended <- all_efiles %>%
  group_by(RecordID) %>%
  mutate(n = n()) %>%
  ungroup() %>%
  filter(n > 1) %>%
  select(-n)

n_years_appeared <- amended %>%
  group_by(RecordID, IndexFile) %>%
  summarise() %>%
  ungroup() %>%
  group_by(RecordID) %>%
  summarise(n_years_appeared = n()) %>%
  ungroup()

amended_eins <- amended %>%
  select(EIN) %>%
  distinct() %>%
  .$EIN

n_periods_for_amended <- all_efiles %>%
  filter(EIN %in% amended_eins) %>%
  select(EIN, RecordID) %>%
  distinct() %>%
  group_by(EIN) %>%
  summarise(n_periods = n()) %>%
  ungroup()

amended <- amended %>%
  left_join(n_years_appeared) %>%
  left_join(n_periods_for_amended) %>%
  arrange(desc(n_years_appeared), desc(n_periods)) 

write_csv(amended, "/dmz/github/analysis/composer/tmp/efile_indices/amended.csv", na="")

retained_eins <- c(
  "943041314",   # 9 periods, amended filing appeared in three different years
  "260687839",   # Amended EZ from pre-2011; 8 periods, amended filing appeared in three different years
  "208419458"    # Amended PF; 9 periods, amended filing appears all in one year
)
retained_efiles <- all_efiles %>%
  filter(EIN %in% retained_eins)

write_csv(retained_efiles, "/dmz/github/analysis/composer/tmp/efile_indices/retained_efiles.csv", na="")
