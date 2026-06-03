from database.DB_connect import DBConnect
from model.Constructor import Constructor


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(a1, a2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.constructorId, c.constructorRef, c.name, c.nationality 
                from constructors c, results r, races r2 
                where c.constructorId = r.constructorId and r.raceId = r2.raceId 
                and r.`position` is not null and r2.`year` >= %s and r2.`year` <= %s"""

        cursor.execute(query, (a1,a2))

        for row in cursor:
            results.append(Constructor(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(a1, a2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select c1.constructorId as cos1, c2.constructorId as cos2, count(distinct c1.driverID) as peso
                    from (select c.constructorId, r.driverId, r2.raceId
		            from constructors c, results r, races r2 
		            where c.constructorId = r.constructorId and r.raceId = r2.raceId 
		            and r.`position` is not null and r2.`year` >= %s and r2.`year` <= %s
		            order by c.constructorId, r.driverId, r2.raceId) c1,
		            (select c.constructorId, r.driverId, r2.raceId
		            from constructors c, results r, races r2 
		        where c.constructorId = r.constructorId and r.raceId = r2.raceId 
		        and r.`position` is not null and r2.`year` >= %s and r2.`year` <= %s
                order by c.constructorId, r.driverId, r2.raceId) c2
                where c1.constructorId < c2.constructorId and c1.raceId <> c2.raceId and c1.driverId = c2.driverId
                group by c1.constructorId, c2.constructorId"""

        cursor.execute(query, (a1, a2, a1, a2))

        for row in cursor:
            results.append((row["cos1"], row["cos2"], row["peso"]))
    #prova
        cursor.close()
        conn.close()
        return results
