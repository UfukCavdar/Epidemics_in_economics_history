library(tidyverse)
library(stargazer)
library(huxtable)
library(lfe)
library(lmtest)
library(sandwich)
library(caret)
library(lubridate)
library(spatstat)

####---- URBAN RURAL POPULATION OLS----

data_epid_pop_2 = read_csv('~/data_to_pop.csv')
data_epid_pop_2 = cbind(data_epid_pop_2, dummify(data_epid_pop_2[c('org_type', 'org_prv')]))

string = ' ~ rkm_1849 + org_type.Stadtkreis + rkm_1849*org_type.Stadtkreis + o_ind_1849 + o_serv_1849 + o_agr_1849 + o_craft_1849 + area + org_prv.Brandenburg + org_prv.Pommern + org_prv.Posen + org_prv.Preussen + org_prv.Rheinland + org_prv.Sachsen + org_prv.Schlesien'

data_epid_pop_2['o_agr_1849'] = data_epid_pop_2['o_agr_1849'] / 1000
data_epid_pop_2['o_serv_1849'] = data_epid_pop_2['o_serv_1849'] / 1000
data_epid_pop_2['o_ind_1849'] = data_epid_pop_2['o_ind_1849'] / 1000
data_epid_pop_2['o_craft_1849'] = data_epid_pop_2['o_craft_1849'] / 1000

mod_pop_31_49_2 = lm(paste('g_31_49', string), data = data_epid_pop_2)
mod_pop_49_75_2 = lm(paste('g_49_75', string), data = data_epid_pop_2)
mod_pop_49_52_2 = lm(paste('g_49_52', string), data = data_epid_pop_2)
mod_pop_52_55_2 = lm(paste('g_52_55', string), data = data_epid_pop_2)
mod_pop_55_61_2 = lm(paste('g_55_61', string), data = data_epid_pop_2)
mod_pop_61_64_2 = lm(paste('g_61_64', string), data = data_epid_pop_2)
mod_pop_64_67_2 = lm(paste('g_64_67', string), data = data_epid_pop_2)
mod_pop_67_71_2 = lm(paste('g_67_71', string), data = data_epid_pop_2)
mod_pop_71_75_2 = lm(paste('g_71_75', string), data = data_epid_pop_2)

robust_se_models_pop_1849 <- list(coef(summary(mod_pop_31_49_2, robust=T))[, 2],
                                  coef(summary(mod_pop_49_75_2, robust=T))[, 2], 
                                  coef(summary(mod_pop_49_52_2, robust=T))[, 2], 
                                  coef(summary(mod_pop_52_55_2, robust=T))[, 2], 
                                  coef(summary(mod_pop_55_61_2, robust=T))[, 2], 
                                  coef(summary(mod_pop_61_64_2, robust=T))[, 2], 
                                  coef(summary(mod_pop_64_67_2, robust=T))[, 2], 
                                  coef(summary(mod_pop_67_71_2, robust=T))[, 2], 
                                  coef(summary(mod_pop_71_75_2, robust=T))[, 2])

stargazer(mod_pop_31_49_2, mod_pop_49_75_2, mod_pop_49_52_2, mod_pop_52_55_2, 
          mod_pop_55_61_2, mod_pop_61_64_2, mod_pop_64_67_2, mod_pop_67_71_2, 
          mod_pop_71_75_2,
          out = "doc.doc",
          style = "aer",
          column.labels = c("1831-1849", "1849-1875", "1849-1852",
                            "1852-1855", "1855-1861", "1861-1864", 
                            "1864-1867", "1867-1871", "1871-1875"),
          dep.var.labels = "Population Growth",
          keep = c('rkm_1849', 'org_type.Stadtkreis', 'rkm_1849*org_type.Stadtkreis',
                   'o_ind_1849','o_serv_1849', 'o_craft_1849', 'o_agr_1849'),
          covariate.labels =  c("Railroad Length in 100 Km", "Urban County", 'Interaction term',
                                "Workforce in Industry (1000)", "Workforce in Service (1000)",
                                'Workforce in Craft (1000)',
                                'Workforce in Agriculture (1000)'),
          report=("vc*sp"),
          se = robust_se_models_pop_1849,
          type = 'text')

####---- URBAN RURAL POPULATION FIXED EFFECT----

data_epid_pop_panel = read_csv('~/data_to_pop_panel.csv')
data_epid_pop_panel = cbind(data_epid_pop_panel, dummify(data_epid_pop_panel[c('org_type', 'org_rbz')]))

string_2 = 'org_rbz.Aachen + org_rbz.Arnsberg + org_rbz.Berlin + org_rbz.Breslau + org_rbz.Bromberg + org_rbz.Danzig + org_rbz.Düsseldorf + org_rbz.Erfurt + org_rbz.Frankfurt + org_rbz.Gumbinnen + org_rbz.Koblenz + org_rbz.Köln + org_rbz.Königsberg + org_rbz.Köslin + org_rbz.Liegnitz + org_rbz.Magdeburg + org_rbz.Marienwerder + org_rbz.Merseburg + org_rbz.Minden + org_rbz.Münster + org_rbz.Oppeln + org_rbz.Posen + org_rbz.Potsdam..excl..Berlin. + org_rbz.Stettin + org_rbz.Stralsund'

formula_pop_1 = as.formula(paste('pop_growth ~ rkm + area', string_2,  ' org_rbz.Trier | Year + org_prv + prv_year', sep = " + "))
formula_pop_2 = as.formula(paste('pop_growth ~ rkm + org_type.Stadtkreis + area', string_2,  ' org_rbz.Trier | Year + org_prv + prv_year', sep = " + "))
formula_pop_3 = as.formula(paste('pop_growth ~ rkm + org_type.Stadtkreis + rkm*org_type.Stadtkreis + area' , string_2,  ' org_rbz.Trier | Year + org_prv + prv_year', sep = " + "))

model_pop_felm_1 = felm(formula_pop_1, data_epid_pop_panel)
model_pop_felm_2 = felm(formula_pop_2, data_epid_pop_panel)
model_pop_felm_3 = felm(formula_pop_3, data_epid_pop_panel)

robust_se_models_pop_fxef <- list(coef(summary(model_pop_felm_1, robust=T))[, 2],
                                  coef(summary(model_pop_felm_2, robust=T))[, 2], 
                                  coef(summary(model_pop_felm_3, robust=T))[, 2])

stargazer(model_pop_felm_1, model_pop_felm_2, model_pop_felm_3,
          out = "doc.doc",
          style = "aer",
          column.labels = c("Baseline Model", "With Urban Dummy", "With Interaction Term"),
          dep.var.labels = "Annualized Population Growth",
          keep = c('rkm', 'org_type.Stadtkreis', 'rkm*org_type.Stadtkreis'),
          covariate.labels =  c("Railroad Length in 100 Km", "Urban County", 
                                'Interaction term'),
          report=("vc*sp"),
          se = robust_se_models_pop_fxef,
          type = 'text')

####---- ALL YEARS CHOLERA SPREAD----

data_panel_epid = read_csv('~/data_to_R.csv')
data_panel_epid_high = read_csv('~/data_to_R_high.csv')
data_panel_epid_too_high = read_csv('~/data_to_R_too_high.csv')

data_panel_epid['rkm'] = data_panel_epid['rkm'] / 100
data_panel_epid_high['rkm'] = data_panel_epid_high['rkm'] / 100
data_panel_epid_too_high['rkm'] = data_panel_epid_too_high['rkm'] / 100

formula_1 = as.formula('chol_deaths ~ rkm + density + pop | id + Year + type_year')
formula_2 = as.formula('chol_deaths ~ rkm + density + pop  + Weighted_Avg| id + Year + type_year')
formula_3 = as.formula('chol_deaths ~ rkm + density + pop  + Weighted_Avg + rkm*Weighted_Avg | id + Year + type_year')

model_1 = felm(formula = formula_1, data = data_panel_epid)
model_2 = felm(formula = formula_2, data = data_panel_epid)
model_3 = felm(formula = formula_3, data = data_panel_epid)

robust_se_models <- list(coef(summary(model_1, robust=TRUE))[, 2], #Robust Standard Error Varience - Covarience matrix
                         coef(summary(model_2, robust=TRUE))[, 2], 
                         coef(summary(model_3, robust=TRUE))[, 2])


railroad_cholera_deaths <- stargazer(model_1, 
                                     model_2, 
                                     model_3,
                                     out = "doc.doc",
                                     style = "aer",
                                     column.labels = c("Baseline Model",
                                                       "With Weighted Avg",
                                                       "With Weighted Avg + Interaction Term"),
                                     dep.var.labels = "Cholera Deaths",
                                     covariate.labels =  c("Railroad Length in 100 Km", "Density",
                                                           "Weighted Avg", "Weighted Avg x Railroad Length in Km"),
                                     report=("vc*sp"),
                                     se = robust_se_models,
                                     type = 'text')

####---- HIGH YEARS CHOLERA SPREAD----

model_1_high = felm(formula = formula_1, data = data_panel_epid_high)
model_2_high = felm(formula = formula_2, data = data_panel_epid_high)
model_3_high = felm(formula = formula_3, data = data_panel_epid_high)

robust_se_models_high <- list(coef(summary(model_1_high, robust=TRUE))[, 2],
                         coef(summary(model_2_high, robust=TRUE))[, 2], 
                         coef(summary(model_3_high, robust=TRUE))[, 2])

railroad_cholera_deaths_high <- stargazer(model_1_high,
                                     model_2_high, 
                                     model_3_high,
                                     out = "doc.doc",
                                     style = "aer",
                                     column.labels = c("Baseline Model",
                                                       "With Weighted Avg",
                                                       "With Weighted Avg + Interaction Term"),
                                     dep.var.labels = "Cholera Deaths",
                                     covariate.labels =  c("Railroad Length in 100 Km", "Population Density",
                                                           "Weighted Avg", "Weighted Avg x Railroad Length in Km"),
                                     report=("vc*sp"),
                                     se = robust_se_models_high,
                                     type = 'text')

####---- TOO HIGH YEARS CHOLERA SPREAD----

model_1_too_high = felm(formula = formula_1, data = data_panel_epid_too_high)
model_2_too_high = felm(formula = formula_2, data = data_panel_epid_too_high)
model_3_too_high = felm(formula = formula_3, data = data_panel_epid_too_high)

robust_se_models_too_high <- list(coef(summary(model_1_too_high, robust=TRUE))[, 2],
                         coef(summary(model_2_too_high, robust=TRUE))[, 2], 
                         coef(summary(model_3_too_high, robust=TRUE))[, 2])

railroad_cholera_deaths_too_high <- stargazer(model_1_too_high,
                                     model_2_too_high, 
                                     model_3_too_high,
                                     out = "doc.doc",
                                     style = "aer",
                                     column.labels = c("Baseline Model",
                                                       "With Weighted Avg",
                                                       "With Weighted Avg + Interaction Term"),
                                     dep.var.labels = "Cholera Deaths",
                                     covariate.labels =  c("Railroad Length in Km", "Population Density",
                                                           "Weighted Avg", "Weighted Avg x Railroad Length in Km"),
                                     report=("vc*sp"),
                                     se = robust_se_models_too_high,
                                     type = 'text')
