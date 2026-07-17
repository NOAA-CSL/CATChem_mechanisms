import yaml
import numpy as np

def convert_rate_parameters(lit_units_config, micm_units_config):
    MOLES_M3_TO_MOLECULES_CM3 = 1.0e-6 *  6.02214076e23
    
    with open(lit_units_config, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    for rxn in config_dict:
        moles_reacted = np.sum([sp.get('coefficient', 1) for sp in rxn.get('reactants', [])])
        if rxn['type'] == 'ARRHENIUS':
            if 'A' in rxn:
                factor = np.power(MOLES_M3_TO_MOLECULES_CM3, moles_reacted - 1)
                rxn['A'] = (float(rxn['A']) * factor).item()
                
        elif rxn['type'] == 'TROE':
            k0_factor = np.power(MOLES_M3_TO_MOLECULES_CM3, moles_reacted)
            kinf_factor = np.power(MOLES_M3_TO_MOLECULES_CM3, moles_reacted - 1)
            
            if 'k0_A' in rxn:
                rxn['k0_A'] = (float(rxn['k0_A']) * k0_factor).item()
                    
            if 'kinf_A' in rxn:
                rxn['kinf_A'] = (float(rxn['kinf_A']) * kinf_factor).item()
    
    with open(micm_units_config, 'w') as f:
        yaml.dump(config_dict, f)

    return

lit_units_config = '/home/mbruckner/catchem/CATChem_mechanisms/mech/AM4.1/user_rxns.yaml'
micm_units_config = '/home/mbruckner/catchem/CATChem_mechanisms/mech/AM4.1/user_rxns_si.yaml'
convert_rate_parameters(lit_units_config, micm_units_config)

lit_units_config = '/home/mbruckner/catchem/CATChem_mechanisms/mech/AM4.1/reactions.yaml'
micm_units_config = '/home/mbruckner/catchem/CATChem_mechanisms/mech/AM4.1/reactions_si.yaml'
convert_rate_parameters(lit_units_config, micm_units_config)