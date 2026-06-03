import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.grafoCreato = False

    def fillDDyears(self):
        year1 = self._model.getAllYears()
        year1OPT = list(map(lambda x: ft.dropdown.Option(x), year1))
        self._view._ddAnno1.options = year1OPT
        print(self._view._ddAnno1.value)
        year2 = self._model.getAllYears()
        year2OPT = list(map(lambda x: ft.dropdown.Option(x), year2))
        self._view._ddAnno2.options = year2OPT
        print(self._view._ddAnno2.value)
        self._view.update_page()


    def handleCreaGrafo(self,e):
        #controlli
        if self._view._ddAnno1.value is None:  # oppure is None per le tendine inizializzo nell'init
            self._view.txt_result.controls.append(
                ft.Text(f"Inserire un anno di inizio", color="red"))
            self._view.update_page()
            return
        if self._view._ddAnno2.value is None:  # oppure is None per le tendine inizializzo nell'init
            self._view.txt_result.controls.append(
                ft.Text(f"Inserire un anno di fine", color="red"))
            self._view.update_page()
            return
        try:
            anno1Int = int( self._view._ddAnno1.value)
            anno2Int = int(self._view._ddAnno2.value)
        except ValueError:
            self._view.txt_result.controls.append(
                ft.Text(f"Inserire un valore numerico", color="red"))
            self._view.update_page()
            return
        if anno1Int > anno2Int:  # oppure is None per le tendine inizializzo nell'init
            self._view.txt_result.controls.append(
                ft.Text(f"Inserire un anno di fine maggipre di quello di inizio", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(anno1Int, anno2Int)
        self.grafoCreato = True
        n, e = self._model.getDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato: "))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {n} \nNumero di archi: {e}"))
        self._view.update_page()


    def handleDettagli(self, e):
        if self.grafoCreato == False:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(f"Costruire il grafo prima di usare questo metodo", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Archi di peso maggiore: ", color="red"))
        archi = self._model.getBestArchi()
        for a in archi:
            self._view.txt_result.controls.append(
                ft.Text(f"{a[0].name} --> {a[1].name} ({a[2]} piloti condivisi)"))
        numConn = self._model.getNumCompConnesse()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {numConn} componenti connesse", color="red"))
        maxCompDecr = self._model.getBestDecresc()
        maxComp = self._model.getBestComp()
        self._view.txt_result.controls.append(
            ft.Text(f"Componente connessa più grande ({len(maxComp)} nodi):", color="red"))
        for n in maxComp:
            self._view.txt_result.controls.append(
                ft.Text(f"{n.constructorRef} ({n.name})"))
        self._view.txt_result.controls.append(
            ft.Text(f"Componente connessa in ordine decrescente:", color="red"))
        for n in maxCompDecr:
            self._view.txt_result.controls.append(
                ft.Text(f"{n[0].constructorRef} ({n[0].name}) (grado = {n[1]})"))
        self._view.update_page()
    def handleCerca(self, e):
        pass

