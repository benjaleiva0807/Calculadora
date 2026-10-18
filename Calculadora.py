def calculadora_ley_ohm():
    while True:
        print("   Calculadora Ley de Ohm   ")
        print("1. Calcular Voltaje (V = I * R)")
        print("2. Calcular Corriente (I = V / R)")
        print("3. Calcular Resistencia (R = V / I)")
        print("4. Salir")
    
        opcion = input("Elije una opcion (1, 2, 3, o 4): ")
        
        if opcion == "1":
            Corriente = float(input("Ingresa la corriente en amperios (I): "))
            Resistencia = float(input("Ingresa la resistencia en Ohmios (R): "))
            Voltaje = Corriente * Resistencia
            print(f"El voltaje (V) es: {Voltaje: .2f}")

        elif opcion == "2":
            Voltaje = float(input("Ingresa el Voltaje en Voltios (V): "))
            Resistencia = float(input("Ingresa la Resistencia en Ohmios (R): "))
            if Resistencia == 0:
                print("Error: La Resistencia (R) no puede ser Cero.")
                
            else: 
                Corriente = Voltaje / Resistencia
                print(f"La Corriente (I) es: {Corriente: .2f}")
        
        elif opcion == "3":
            Voltaje = float(input("Ingresa el Voltaje en Voltios (V): "))    
            Corriente = float(input("Ingresa la corriente en amperios (I): "))
            if Corriente == 0:
                print(f"Error: La Corriente (I) no puede ser 0.")
            else:
                Resistencia = Voltaje / Corriente
                print(f"La Resistencia (R) es: {Resistencia: .2f} Ω")
        elif opcion == "4":
            print("Hasta Luego")
            break
        
        else:
            print("Opcion no valida. Por favor, selecciona 1, 2, o 3")
                   
calculadora_ley_ohm()     

