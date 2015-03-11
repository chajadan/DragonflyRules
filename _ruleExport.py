import _quickRules
import inspect


# decorator
def ExportedRule(exportedRulesContainer):
    def ContainerFiller(ruleInstanceOrClass):
        exportedRulesContainer.add(ruleInstanceOrClass)
    return ContainerFiller
        
class ExportedRules():
    def __init__(self):
        self.ruleList = []
    
    def add(self, ruleInstanceOrClass):
        if inspect.isclass(ruleInstanceOrClass):
            if issubclass(ruleInstanceOrClass, (_quickRules.QuickRules, _quickRules.QuickContinuousRules)):
                self.ruleList.append(ruleInstanceOrClass)
            else:
                self.ruleList.append(ruleInstanceOrClass())
        else:
            self.ruleList.append(ruleInstanceOrClass)
            
class ExportedLang(ExportedRules):
    def __init__(self, language_name):
        self.language_name = language_name
        ExportedRules.__init__(self)